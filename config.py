import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Debug print
print(f"API_ID: {os.getenv('API_ID')}")  # This will show what is being loaded

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", "0"))  # Default to 0 if not found
API_HASH = os.environ.get("API_HASH", "")
DB_URI = os.environ.get("DB_URI", "")
