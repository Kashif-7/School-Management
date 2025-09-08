
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import app, db
from app.model import models

if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
