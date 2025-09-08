import os
from dotenv import load_dotenv

# Load environment variables before importing the app
load_dotenv()

from app import app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    app.run(host="0.0.0.0", port=port)
