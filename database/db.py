from motor.motor_asyncio import AsyncIOMotorClient
import os

# Create a global variable for the database connection
db_client = None
db = None

async def initialize_db():
    """
    Initialize the database connection.
    """
    global db_client, db
    db_uri = os.getenv("DB_URI")  # Ensure DB_URI is in your .env file
    if not db_uri:
        raise ValueError("DB_URI is not set. Please check your environment variables.")
    
    db_client = AsyncIOMotorClient(db_uri)
    db = db_client.get_database()  # Access default database in the URI
    print("Database connection initialized.")
