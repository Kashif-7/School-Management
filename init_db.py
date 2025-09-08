"""
Initialize the PostgreSQL database for the School Management System.
This script creates all the necessary tables in the database.
"""

from app import app, db
from app.model import models

if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
