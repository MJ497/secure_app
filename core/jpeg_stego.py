import cv2
import numpy as np

# Delimiter used to mark end of payload
DELIMITER = "#####"


# ================= CAPACITY =================

def jpeg_capacity(image_path):
    """
    Returns maximum number of bits that can be embedded
    (1 bit per pixel per channel for LSB steganography).
    Uses blue channel for embedding to preserve color.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read image")
    h, w = img.shape[:2]
    return (h * w)  # bits (1 per pixel in blue channel)


# ================= BIT HELPERS =================

def _to_bits(data: bytes):
    return ''.join(format(byte, '08b') for byte in data)


def _from_bits(bits: str):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


# ================= EMBED =================

def embed_jpeg_dct(image_path, secret_data: bytes, output_path):
    """
    Embed encrypted data into image using LSB steganography on blue channel.
    Preserves color by only modifying LSB of blue channel.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read image")
    
    # Prepare data with delimiter
    data_with_delim = secret_data + DELIMITER.encode()
    bits = _to_bits(data_with_delim)
    
    # Use blue channel (index 0 in BGR)
    blue_channel = img[:, :, 0].flatten()
    
    # Check capacity
    if len(bits) > len(blue_channel):
        raise ValueError("Data too large for image")
    
    # Embed bits into LSB of blue channel
    for i, bit in enumerate(bits):
        blue_channel[i] = (blue_channel[i] & 0xFE) | int(bit)
    
    # Reshape and put back
    img[:, :, 0] = blue_channel.reshape(img.shape[:2])
    cv2.imwrite(output_path, img)
    
    return True


# ================= EXTRACT =================

def extract_jpeg_dct(image_path):
    """
    Extract hidden data from image using LSB steganography on blue channel.
    Stops automatically when delimiter is found.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read image")
    
    # Extract from blue channel (index 0 in BGR)
    blue_channel = img[:, :, 0].flatten()
    
    bits = ""
    extracted = bytearray()
    
    # Extract LSB from each pixel in blue channel
    for pixel in blue_channel:
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
