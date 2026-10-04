import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SECRET_KEY = os.getenv("SECRET_KEY", "comiccraft_secret_key_123")

EXPORT_FOLDER = os.path.join("app", "static", "exports")
PANELS_FOLDER = os.path.join("app", "static", "panels")
FONT_PATH = "DejaVuSans.ttf"

os.makedirs(EXPORT_FOLDER, exist_ok=True)
os.makedirs(PANELS_FOLDER, exist_ok=True)