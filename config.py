import os

# Bot token from @BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Telegram API credentials from my.telegram.org
API_ID = int(os.environ.get("API_ID", "24210243"))
API_HASH = os.environ.get("API_HASH", "509031fb3790b968e489f71d591ebce5")

# MongoDB URI
DB_URI = os.environ.get("DB_URI", "")  # MongoDB connection string
DB_NAME = "bot_database"  # Default database name
