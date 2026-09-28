import os
import base64
import time

from flask import (
    Flask, request, send_file,
    render_template, redirect, url_for, session
)
from werkzeug.utils import secure_filename

from config import Config
from core.crypto import generate_key, encrypt_data, decrypt_data
from core.stego import embed_data, extract_data           # PNG-LSB
from core.jpeg_stego import (
    embed_jpeg_dct,
    extract_jpeg_dct,
    jpeg_capacity,
    DELIMITER
)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "super_secret_session_key"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ================= AUTH GUARD =================

@app.before_request
def require_login():
    public_routes = ['login', 'static']
    if request.endpoint not in public_routes and 'user' not in session:
        return redirect(url_for('login'))

# ================= AUTH =================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (
            request.form.get('username') == 'admin' and
            request.form.get('password') == 'admin123'
        ):
            session['user'] = 'admin'
            return redirect(url_for('home'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= PAGES =================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encode', methods=['GET'])
def encode_page():
    return render_template('encode.html')


@app.route('/decode', methods=['GET'])
def decode_page():
    return render_template('decode.html')

# ================= ENCODE =================

@app.route('/encode', methods=['POST'])
def encode():
    file = request.files.get('file')
    image = request.files.get('image')

    if not file or not image:
        return render_template('encode.html', error="File and image required")

    file_name = secure_filename(file.filename)
    image_name = secure_filename(image.filename)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

    file.save(file_path)
    image.save(image_path)

    with open(file_path, 'rb') as f:
        raw_data = f.read()

    key = generate_key()
    encrypted = encrypt_data(key, raw_data)
    encoded_key = base64.b64encode(key).decode()

    ext = image_name.rsplit('.', 1)[1].lower()
    output_image = os.path.join(
        app.config['UPLOAD_FOLDER'],
        f"encoded_{image_name}"
    )

    start = time.time()

    try:
        # ---------- PNG (LSB) ----------
        if ext == 'png':
            embed_data(image_path, encrypted, output_image)

        # ---------- JPEG (DCT) ----------
        elif ext in ['jpg', 'jpeg']:
            required_bits = (len(encrypted) + len(DELIMITER)) * 8
            capacity = jpeg_capacity(image_path)

            if required_bits > capacity:
                return render_template(
                    'encode.html',
                    error="Payload too large for this JPEG image"
                )

            embed_jpeg_dct(image_path, encrypted, output_image)

        else:
            return render_template(
                'encode.html',
                error="Unsupported image format"
            )

    except Exception as e:
        print("ENCODE ERROR:", e)
        return render_template(
            'encode.html',
            error="Encoding failed. Check image format and payload size."
        )

    print("Encoding time:", time.time() - start)

    return render_template(
        'result.html',
        message="Encoding successful. SAVE THE SECRET KEY. Note : key cannot be regenerated.",
        secret_key=encoded_key,
        download_url=url_for(
            'download_file',
            filename=os.path.basename(output_image)
        )
    )

# ================= DECODE =================

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files.get('image')
    key_input = request.form.get('key')

    if not image or not key_input:
        return render_template('decode.html', error="Image and key required")

    try:
        key = base64.b64decode(key_input)
    except Exception:
        return render_template('decode.html', error="Invalid key format")

    image_name = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    image.save(image_path)

    ext = image_name.rsplit('.', 1)[1].lower()

    try:
        if ext == 'png':
            encrypted = extract_data(image_path)

        elif ext in ['jpg', 'jpeg']:
            encrypted = extract_jpeg_dct(image_path)

        else:
            return render_template(
                'decode.html',
                error="Unsupported image format"
            )

        decrypted = decrypt_data(key, encrypted)

    except Exception:
        return render_template(
            'decode.html',
            error="Wrong key or corrupted image"
        )

    output_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        "decoded_file"
    )

    with open(output_path, 'wb') as f:
        f.write(decrypted)

    return send_file(
        output_path,
        as_attachment=True,
        download_name="decoded_file"
    )

# ================= DOWNLOAD =================

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
