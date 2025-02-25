# ---------------------------------------------------
# File Name: users_db.py
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

from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_DB)
db = mongo.users
db = db.users_db


async def get_users():
  user_list = []
  async for user in db.users.find({"user": {"$gt": 0}}):
    user_list.append(user['user'])
  return user_list


async def get_user(user):
  users = await get_users()
  if user in users:
    return True
  else:
    return False

async def add_user(user):
  users = await get_users()
  if user in users:
    return
  else:
    await db.users.insert_one({"user": user})


async def del_user(user):
  users = await get_users()
  if not user in users:
    return
  else:
    await db.users.delete_one({"user": user})
    

async def remove_ban(user_id):
    await users_col.update_one(
        {'user': user_id}, {'$set': {'ban_status': {"is_banned": False, "ban_reason": ""}}}
    )

async def ban_user(user_id, ban_reason="No Reason"):
    await users_col.update_one(
        {'user': user_id}, {'$set': {'ban_status': {"is_banned": True, "ban_reason": ban_reason}}}
    )

async def get_ban_status(user_id):
    user = await users_col.find_one({'user': user_id}, {"_id": 0, "ban_status": 1})
    return user.get('ban_status', {"is_banned": False, "ban_reason": ""}) if user else {"is_banned": False, "ban_reason": ""}
