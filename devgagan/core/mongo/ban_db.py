# ---------------------------------------------------
# File Name: ban_db.py
# Description: Handles ban-related database operations for the Pyrogram bot.
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

class BanDB:
    def __init__(self):
        self.mongo = MongoCli(MONGO_DB)
        self.db = self.mongo.ban_db
        self.collection = self.db.banned_users  # Define the collection explicitly

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = {"is_banned": True, "ban_reason": ban_reason}
        await self.collection.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}}, upsert=True)

    async def unban_user(self, user_id):
        await self.collection.update_one({"id": user_id}, {"$set": {"ban_status": {"is_banned": False, "ban_reason": ""}}})

    async def get_ban_status(self, user_id):
        default = {"is_banned": False, "ban_reason": ""}
        user = await self.collection.find_one({"id": user_id})
        return user.get("ban_status", default) if user else default

    async def ban_chat(self, chat_id, reason="No Reason"):
        await self.collection.update_one({"chat_id": chat_id}, {"$set": {"is_banned": True, "reason": reason}}, upsert=True)

    async def unban_chat(self, chat_id):
        await self.collection.update_one({"chat_id": chat_id}, {"$set": {"is_banned": False, "reason": ""}}})

    async def get_chat_ban_status(self, chat_id):
        chat = await self.collection.find_one({"chat_id": chat_id})
        return chat.get("is_banned", False) if chat else False
