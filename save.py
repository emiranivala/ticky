import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import database
from nondatabase.strings import strings
from nondatabase.download_large_file import split_large_file

async def download_status(client, statusfile, message):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as f:
            progress = f.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Downloaded: {progress}")
        except:
            pass
        await asyncio.sleep(10)

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply(strings["welcome"])

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply(strings["help"])

@Client.on_message(filters.text & filters.private)
async def save_restricted(client: Client, message: Message):
    if "https://t.me/" not in message.text:
        await message.reply("Invalid link.")
        return

    # Parse the link
    link_parts = message.text.split("/")
    chat_username = link_parts[3]
    msg_id = int(link_parts[4].split("-")[0])

    try:
        msg = await client.get_messages(chat_username, msg_id)
        smsg = await message.reply("Downloading...")
        file_path = await client.download_media(msg, progress=lambda c, t: open(f"{message.id}_downstatus.txt", "w").write(f"{c * 100 / t:.1f}%"))

        if os.path.getsize(file_path) > 2 * 1024 * 1024 * 1024:  # If file > 2GB, split
            parts = split_large_file(file_path)
            for part in parts:
                await client.send_document(message.chat.id, part, caption="Part of a large file")
                os.remove(part)
        else:
            await client.send_document(message.chat.id, file_path)
        os.remove(file_path)

        if os.path.exists(f"{message.id}_downstatus.txt"):
            os.remove(f"{message.id}_downstatus.txt")
    except Exception as e:
        await message.reply(f"Error: {e}")
