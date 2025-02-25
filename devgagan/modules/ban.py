import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from devgagan.core.mongo import ban_db as ban_db
import pytz
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from devgagan import app
from config import OWNER_ID

# Initialize BanDB
ban_db = ban_db.BanDB()

# Load banned users and chats from the database
BANNED_USERS = []
BANNED_CHATS = []

async def load_banned_users():
    global BANNED_USERS
    users = await ban_db.db.find({"ban_status.is_banned": True}).to_list(None)
    BANNED_USERS = [user["id"] for user in users]

async def load_banned_chats():
    global BANNED_CHATS
    chats = await ban_db.db.find({"is_banned": True}).to_list(None)
    BANNED_CHATS = [chat["chat_id"] for chat in chats]

# Load banned users and chats when the bot starts
app.on_startup(load_banned_users)
app.on_startup(load_banned_chats)

@app.on_message(filters.command('ban') & filters.user(OWNER_ID))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure I have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure it's a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await ban_db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await ban_db.ban_user(k.id, reason)
        BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")

@app.on_message(filters.command('unban') & filters.user(OWNER_ID))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure I have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure it's a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await ban_db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await ban_db.unban_user(k.id)
        BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")

# Ban/Unban Chat Functions
@app.on_message(filters.command('banchat') & filters.user(OWNER_ID))
async def ban_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat_id = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason Provided"
    await ban_db.ban_chat(chat_id, reason)
    BANNED_CHATS.append(chat_id)
    await message.reply(f"Successfully banned chat {chat_id}")

@app.on_message(filters.command('unbanchat') & filters.user(OWNER_ID))
async def unban_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat_id = message.command[1]
    await ban_db.unban_chat(chat_id)
    BANNED_CHATS.remove(chat_id)
    await message.reply(f"Successfully unbanned chat {chat_id}")

# Filters for banned users and chats
async def banned_users(_, client, message: Message):
    return message.from_user and message.from_user.id in BANNED_USERS

async def disabled_chat(_, client, message: Message):
    return message.chat.id in BANNED_CHATS

banned_user = filters.create(banned_users)
disabled_group = filters.create(disabled_chat)

# Ban Reply for Banned Users
@app.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    buttons = [[
        InlineKeyboardButton('Support', url=f'https://t.me/Mr_MAHIji/18/')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    ban = await ban_db.get_ban_status(message.from_user.id)
    await message.reply(
        text=f"Sorry Dude, You are Banned to use Me. \nBan Reason: {ban['ban_reason']}",
        reply_markup=reply_markup)

# Ban Reply for Banned Chats
@app.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('Support', url=f'https://t.me/Mr_MAHIji/18/')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    vazha = await ban_db.get_chat_ban_status(message.chat.id)
    k = await message.reply(
        text=f"CHAT NOT ALLOWED 🐞\n\nMy admins have restricted me from working here! If you want to know more about it, contact support.\nReason: <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
