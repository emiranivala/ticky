import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the MongoDB URI from the environment variables
db_uri = os.getenv("DB_URI")

# Initialize MongoDB client
db_client = AsyncIOMotorClient(db_uri)

# Function to initialize the database
async def initialize_db():
    global db
    db = db_client.get_database()  # Automatically use the database defined in the URI
    print(f"Connected to database: {db.name}")

