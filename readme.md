Secure Image-Based Steganography System Using Flask
Project Overview

This project is a secure web-based steganography system built using Python (Flask), HTML, and CSS. It allows users to hide secret files inside images and later extract them using a secret key.

The system combines:

Steganography — hiding information inside images

Cryptography — encrypting the secret file

Web application architecture — using Flask framework

Security design principles — key-based data protection

This project is developed as a BSc graduate-level academic project, focusing on data security, privacy, and secure communication.

Key Features

Hide any file inside an image securely

AES-based encryption of hidden data

Unique secret key generation per encoding

Secure extraction using secret key

Simple and clean web interface

Downloadable encoded image

Automatic file handling and cleanup
Technologies Used
Backend

Python 3.10+

Flask

Pillow (Image processing)

Cryptography (AES encryption)

Steganography algorithms (LSB-based encoding)

Frontend

HTML5

CSS3 (custom styling)

How The System Works
Encoding Process

User uploads:

A cover image (PNG format)

A secret file (text, pdf, zip, etc.)

The secret file is:

Encrypted using AES encryption

Embedded inside the image using steganography

A unique secret key is generated.

The encoded image is made available for download.

Decoding Process

User uploads:

Encoded image

Secret key

The system:

Extracts encrypted data

Decrypts using the key

Original file is restored and downloaded.
Security Design

AES-256 encryption protects the hidden data

Each encoding generates a unique secret key

No secret keys are stored on the server

Temporary files are automatically deleted

Steganographic concealment prevents detection