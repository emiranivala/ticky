from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch environment variables with validation
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH")
DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME", "bot_database")  # Default value if DB_NAME is not provided

# Validate mandatory variables
if not all([BOT_TOKEN, API_ID, API_HASH, DB_URI]):
    raise EnvironmentError("One or more required environment variables are missing!")
