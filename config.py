import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token from @Botfather
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Your API ID from my.telegram.org
API_ID = int(os.getenv("API_ID", "20259558"))

# Your API Hash from my.telegram.org
API_HASH = os.getenv("API_HASH", "ce95ed6fecb559fecbb6fb7ebed176e4")

# Database URI
DB_URI = os.getenv("DB_URI", "")
