import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB upload limit

    UPLOAD_FOLDER = "uploads"
    ALLOWED_IMAGE_EXTENSIONS = {"png"}
    ALLOWED_FILE_EXTENSIONS = {"txt", "pdf", "zip", "bin", "docx", "png"}
