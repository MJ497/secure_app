import cv2
import numpy as np

# Delimiter used to mark end of payload
DELIMITER = "#####"


# ================= CAPACITY =================

def jpeg_capacity(image_path):
    """
    Returns maximum number of bits that can be embedded
    (1 bit per pixel for LSB steganography).
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    return (h * w)  # bits (1 per pixel)


# ================= BIT HELPERS =================

def _to_bits(data: bytes):
    return ''.join(format(byte, '08b') for byte in data)


def _from_bits(bits: str):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


# ================= EMBED =================

def embed_jpeg_dct(image_path, secret_data: bytes, output_path):
    """
    Embed encrypted data into image using LSB (Least Significant Bit) steganography.
    More reliable than DCT for JPEG images.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Prepare data with delimiter
    data_with_delim = secret_data + DELIMITER.encode()
    bits = _to_bits(data_with_delim)
    
    # Flatten image
    flat_img = img.flatten()
    
    # Check capacity
    if len(bits) > len(flat_img):
        raise ValueError("Data too large for image")
    
    # Embed bits into LSB of each pixel
    for i, bit in enumerate(bits):
        flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
    
    # Reshape and save
    embedded_img = flat_img.reshape(img.shape)
    cv2.imwrite(output_path, embedded_img)
    
    return True


# ================= EXTRACT =================

def extract_jpeg_dct(image_path):
    """
    Extract hidden data from image using LSB steganography.
    Stops automatically when delimiter is found.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    flat_img = img.flatten()
    
    bits = ""
    extracted = bytearray()
    
    # Extract LSB from each pixel
    for pixel in flat_img:
        bit = pixel & 1
        bits += str(bit)
        
        if len(bits) == 8:
            byte = int(bits, 2)
            extracted.append(byte)
            bits = ""
            
            # Check if we've found the delimiter
            if extracted.endswith(DELIMITER.encode()):
                return bytes(extracted[:-len(DELIMITER)])
    
    # If we get here, delimiter was never found
    raise ValueError("Delimiter not found – corrupted or invalid image")
