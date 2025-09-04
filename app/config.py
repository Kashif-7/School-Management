import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CREDENTIALS = {
        "DB_USER": os.getenv("DB_USER"),
        "DB_PW": os.getenv("DB_PW"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": int(os.getenv("DB_PORT", 27017)),
        "DB_NAME": os.getenv("DB_NAME"),
    }
