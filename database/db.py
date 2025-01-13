import motor.motor_asyncio
from config import DB_URI, DB_NAME

class Database:
    def __init__(self, uri, db_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[db_name]

    # Define your database methods here

# Initialize the database
db = Database(DB_URI, DB_NAME)

async def initialize_db():
    print(f"Connected to database: {db.db.name}")
