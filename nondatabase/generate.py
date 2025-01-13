import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from asyncio.exceptions import TimeoutError
from config import API_ID, API_HASH
from database.db import db

# String session size threshold
SESSION_STRING_SIZE = 351

# Utility function for safe dictionary access
def get(obj, key, default=None):
    return obj.get(key, default) if obj else default

# Logout Command
@Client.on_message(filters.private & filters.command("logout"))
async def logout(client: Client, message: Message):
    """Handles the /logout command."""
    try:
        user_data = await db.is_user_exist(message.chat.id)
        if not user_data or not await db.get_session(message.chat.id):
            await message.reply("You are not logged in.")
            return

        await db.set_session(message.chat.id, None)
        await message.reply("**Logout Successful!**")
    except Exception as e:
        await message.reply(f"<b>Error during logout:</b> {e}")

# Login Command
@Client.on_message(filters.private & filters.command("login"))
async def login(client: Client, message: Message):
    """Handles the /login command."""
    user_id = message.chat.id

    try:
        # Check if the user exists and is already logged in
        if await db.is_user_exist(user_id):
            user_data = await db.get_session(user_id)
            if user_data:
                await message.reply("You are already logged in.")
                return
        else:
            # Add the user to the database if not exists
            await db.add_user(user_id, message.from_user.first_name)

        # Ask for the phone number
        phone_number_msg = await client.ask(
            chat_id=user_id,
            text="<b>Send your phone number including country code (e.g., +13124562345).</b>\n\nType /cancel to cancel the process.",
            timeout=300
        )
        if phone_number_msg.text.strip().lower() == '/cancel':
            await phone_number_msg.reply("<b>Process cancelled.</b>")
            return

        phone_number = phone_number_msg.text.strip()
        client_temp = Client(":memory:", api_id=API_ID, api_hash=API_HASH)

        await client_temp.connect()
        await phone_number_msg.reply("Sending OTP...")
        code = await client_temp.send_code(phone_number)

        # Ask for the OTP
        phone_code_msg = await client.ask(
            user_id,
            "<b>Enter the OTP sent to your Telegram account. Format: '1 2 3 4 5'</b>\n\nType /cancel to cancel.",
            filters=filters.text,
            timeout=600
        )
        if phone_code_msg.text.strip().lower() == '/cancel':
            await phone_code_msg.reply("<b>Process cancelled.</b>")
            return

        phone_code = phone_code_msg.text.replace(" ", "")
        await client_temp.sign_in(phone_number, code.phone_code_hash, phone_code)

    except (PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired) as e:
        await message.reply(f"<b>Error:</b> {e}")
        return

    except SessionPasswordNeeded:
        # Handle two-step verification
        two_step_msg = await client.ask(
            user_id,
            "<b>Two-step verification is enabled. Enter your password.</b>\n\nType /cancel to cancel.",
            filters=filters.text,
            timeout=300
        )
        if two_step_msg.text.strip().lower() == '/cancel':
            await two_step_msg.reply("<b>Process cancelled.</b>")
            return

        try:
            await client_temp.check_password(password=two_step_msg.text)
        except PasswordHashInvalid:
            await two_step_msg.reply("Invalid password.")
            return

    except Exception as e:
        await message.reply(f"<b>Unexpected Error:</b>\n<code>{traceback.format_exc()}</code>")
        return

    # Export the session string
    try:
        string_session = await client_temp.export_session_string()
        await client_temp.disconnect()

        if len(string_session) < SESSION_STRING_SIZE:
            await message.reply("Invalid session string.")
            return

        # Save session string to database
        await db.set_session(user_id, string_session)
        await message.reply("<b>Account logged in successfully.</b>")

    except Exception as e:
        await message.reply(f"<b>Error during login:</b> {e}")
