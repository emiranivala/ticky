

# Initialize the database
DB_URI = "your_mongodb_uri_here"
DB_NAME = "your_database_name_here"

db = Database(DB_URI, DB_NAME)

import motor.motor_asyncio

class Database:
    def __init__(self, uri, database_name):
        """
        Initialize the database connection and set up the users collection.
        """
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users  # Users collection

    async def initialize_db(self):
        """
        Optional: Ensure the database connection is alive.
        """
        try:
            # Simple ping to check if the database connection works
            await self.db.command("ping")
            print("Database connection initialized.")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    async def is_user_exist(self, user_id):
        """
        Check if a user exists in the database.
        """
        user = await self.col.find_one({'id': int(user_id)})
        return bool(user)

    async def add_user(self, user_id, name):
        """
        Add a new user to the database.
        """
        user = {"id": int(user_id), "name": name, "session": None}
        await self.col.insert_one(user)

    async def set_session(self, user_id, session):
        """
        Set or update the session string for a user.
        """
        await self.col.update_one({'id': int(user_id)}, {'$set': {'session': session}})

    async def get_session(self, user_id):
        """
        Retrieve the session string for a user.
        """
        user = await self.col.find_one({'id': int(user_id)})
        return user['session'] if user else None
