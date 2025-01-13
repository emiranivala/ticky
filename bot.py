from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database.db import initialize_db  # Import database initialization

class Bot(Client):
    def __init__(self):
        super().__init__(
            "tricky_login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="nondatabase"),
            workers=50,
            sleep_threshold=10
        )
        initialize_db()  # Initialize the database connection when bot starts

    async def start(self):
        await super().start()
        print('Bot Started Powered By @She_who_remain')

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

Bot().run()
