import base64
from stegano import lsb
from PIL import Image


def calculate_capacity(image_path: str) -> int:
    """
    Calculates how many bytes can be hidden inside the image.
    """
    img = Image.open(image_path)
    width, height = img.size

    # Each pixel has 3 color channels → we use 1 bit per channel
    total_bits = width * height * 3
    return total_bits // 8  # convert bits → bytes

    
def embed_data(image_path: str, data: bytes, output_path: str):
    """
    Embeds encrypted data into an image.
    """
    encoded = base64.b64encode(data).decode('utf-8')

    capacity = calculate_capacity(image_path)
    if len(encoded) > capacity:
        raise ValueError("Data too large for selected image")

    secret_image = lsb.hide(image_path, encoded)
    secret_image.save(output_path)


def extract_data(image_path: str) -> bytes:
    """
    Extracts hidden data from image.
    """
    extracted = lsb.reveal(image_path)

    if extracted is None:
        raise ValueError("No hidden data found")

    return base64.b64decode(extracted)
"""  """