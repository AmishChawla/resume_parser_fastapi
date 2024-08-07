from dotenv import load_dotenv
import os
import stripe
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMIL_PASSWORD")
STRIPE_API_KEY = os.getenv("STRIPE_SECRET_KEY")

# FLASK_URL = 'http://127.0.0.1:5000'


ALLOWED_MIMETYPES = (
    "image/jpeg",
    "image/png",
    "image/gif",
    "video/mp4",
    "video/webm",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


FLASK_URL = 'http://35.154.190.245:5000'





