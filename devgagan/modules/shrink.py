 
# ---------------------------------------------------
# File Name: shrink.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import logging
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
 
 
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
 
Param = {}
 
async def pass_user(message: str, user_id: int) -> int:
    user: Set[int] = await premium_users()
    if user_id in user or user_id in OWNER_ID:
        return 0
    else:
        return 1


async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
 
 
async def get_shortened_url(deep_link):
    # Randomly select a service
    index = random.randint(0, len(WEBSITE_URL) - 1)
    selected_url = WEBSITE_URL[index]
    selected_api = AD_API[index]

    # Construct the API URL
    api_url = f"https://{selected_url}/api?api={selected_api}&url={deep_link}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success":
                        return data.get("shortenedUrl")
                else:
                    logging.error(f"Failed to shorten URL. Status: {response.status}, Response: {await response.text()}")
    except aiohttp.ClientError as e:
        logging.error(f"An error occurred while making the request: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return None
 
 
async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 
 
@app.on_message(filters.command("start"))
async def start_command(client, message):
#async def token_handler(client, message):
    """Handle the /token command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    chat_id = "save_restricted_content_bots"
    msg = await app.get_messages(chat_id, 796)
    user_id = message.chat.id
    user = message.from_user.mention
    if len(message.command) <= 1:
        image_url = "https://envs.sh/tZO.jpg"
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/+055Dfay4AsNjYWE1")
        premium = InlineKeyboardButton("Get Premium", url="https://t.me/Mr_Mahiji")   
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium]    
        ])
         
        await message.reply_photo(
            #msg.photo.file_id,
            image_url,
            caption=(
                f"👋 ʜᴇʟʟᴏ {user},\n"
                "✨ɪ ᴀᴍ ᴀ ʙᴏᴛ ᴅᴇsɪɢɴᴇᴅ ғᴏʀ ʀᴇsᴛʀɪᴄᴛɪᴏɴ ᴘᴜʀᴘᴏsᴇs, ᴄᴀᴘᴀʙʟᴇ ᴏғ sᴀᴠɪɴɢ ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ғɪʟᴇs, ᴍᴇᴅɪᴀ, ᴀɴᴅ ᴍᴏʀᴇ ғʀᴏᴍ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟs.\n\n"
                "✳️ I ᴄᴀɴ sᴀᴠᴇ ᴘᴏsᴛs ғʀᴏᴍ ᴄʜᴀɴɴᴇʟs ᴏʀ ɢʀᴏᴜᴘs ᴡʜᴇʀᴇ ғᴏʀᴡᴀʀᴅɪɴɢ ɪs ᴏғғ.\n"
                "✳️ Sɪᴍᴘʟʏ sᴇɴᴅ ᴛʜᴇ ᴘᴏsᴛ ʟɪɴᴋ ᴏғ ᴀ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟ. Fᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟs, ғɪʀsᴛ Lᴏɢɪɴ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴜsɪɴɢ /login ᴄᴏᴍᴍᴀɴᴅ.\n\n"
                "✨ Sᴇɴᴅ /settings ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ."
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
 
     
    if param:
        if user_id in Param and Param[user_id] == param:
             
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return
 
@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
     
    freecheck = await pass_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active enjoy!")
    else:
         
        param = await generate_random_param()
        Param[user_id] = param   
 
         
        deep_link = f"https://t.me/{client.me.username}?start={param}"
 
         
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return
 
         
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✅ ᴠᴇʀɪғʏ ✅", url=shortened_url)]],
        )
        #await message.reply("Click the button below to verify your free access token: \n\n> What will you get ? \n1. No time bound upto 3 hours \n2. Batch command limit will be FreeLimit + 20 \n3. All functions unlocked"\n\n [ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ❓](https://t.me/Mahi_Botz/23250), reply_markup=button)
        await message.reply(
            "Click the button below to verify your free access token:\n\n"
            "> What will you get ?\n"
            "1. No time Gap BTW links\n"
            "2. **Become Premium user for 3 hours**\n"
            "3. All functions unlocked\n\n"
            "👀    **[ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ❓](https://t.me/Mahi_Bots/23250)**   👀", 
            reply_markup=button,
            disable_web_page_preview=True
        )
