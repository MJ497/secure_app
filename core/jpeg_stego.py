import cv2
import numpy as np

DELIMITER = "#####"

def jpeg_capacity(image_path):
    import cv2
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    return (h * w) // 64  # 1 bit per 8x8 block


def _to_bits(data: bytes):
    return ''.join(format(byte, '08b') for byte in data)

def _from_bits(bits: str):
    bytes_out = []
    for i in range(0, len(bits), 8):
        bytes_out.append(int(bits[i:i+8], 2))
    return bytes(bytes_out)

def embed_jpeg_dct(image_path, secret_data: bytes, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = np.float32(img)

    h, w = img.shape
    bits = _to_bits(secret_data + DELIMITER.encode())
    bit_index = 0

    for i in range(0, h - 8, 8):
        for j in range(0, w - 8, 8):
            block = img[i:i+8, j:j+8]
            dct = cv2.dct(block)

            if bit_index < len(bits):
                dct[4][4] = int(dct[4][4]) | int(bits[bit_index])
                bit_index += 1

            img[i:i+8, j:j+8] = cv2.idct(dct)

            if bit_index >= len(bits):
                break
        if bit_index >= len(bits):
            break

    cv2.imwrite(output_path, img)
    return True


def extract_jpeg_dct(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = np.float32(img)

    bits = ""

    h, w = img.shape
    for i in range(0, h - 8, 8):
        for j in range(0, w - 8, 8):
            block = img[i:i+8, j:j+8]
            dct = cv2.dct(block)
            bits += str(int(dct[4][4]) & 1)

    data = _from_bits(bits)
    return data.split(DELIMITER.encode())[0]
