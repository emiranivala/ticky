import motor.motor_asyncio

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users  # The collection for users

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def add_user(self, id, name):
        user = {"id": id, "name": name, "session": None}
        await self.col.insert_one(user)

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['session'] if user else None

# Initialize the database
DB_URI = "your_mongodb_uri_here"
DB_NAME = "your_database_name_here"

db = Database(DB_URI, DB_NAME)
