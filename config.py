
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Loaded from .env
API_ID = int(os.getenv("API_ID", 0))  # Loaded from .env
API_HASH = os.getenv("API_HASH")  # Loaded from .env
DB_URI = os.getenv("DB_URI")  # Loaded from .env
DB_NAME = os.getenv("DB_NAME", "bot_database")  # Default if not in .env

# Validate mandatory variables
if not all([BOT_TOKEN, API_ID, API_HASH, DB_URI]):
    raise EnvironmentError("One or more required environment variables are missing!")

