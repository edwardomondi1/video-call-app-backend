import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        # Temporary fallback for deployment - set proper env vars in production
        SECRET_KEY = "temp-secret-key-change-in-production"
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'video_call.db'}"
    ).replace("\\", "/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        # Temporary fallback for deployment - set proper env vars in production
        JWT_SECRET_KEY = "temp-jwt-secret-change-in-production"
    
    PORT = int(os.getenv("PORT", 5002))
