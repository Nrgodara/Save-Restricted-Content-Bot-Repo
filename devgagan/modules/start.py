# ---------------------------------------------------
# File Name: start.py
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

from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from devgagan.core.func import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
 
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("cancel", "🚫 Cancel batch process"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        #BotCommand("adl", "👻 Download audio from 30+ sites"),
        #BotCommand("dl", "💀 Download videos from 30+ sites"),
        #BotCommand("pay", "₹ Pay now to get subscription"),
       # BotCommand("status", "⟳ Refresh Payment status"),
       # BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("session", "🧵 Generate Pyrogramv2 session"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("plan", "🗓️ Check our premium plans"),
       # BotCommand("help", "❓ If you're a noob, still!"),
     #   BotCommand("terms", "🥺 Terms and conditions"),
        #BotCommand("speedtest", "🚅 Speed of server"),
        #BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("broadcast", "⚡ Broadcast message to bot users (Admin Only)"),
        BotCommand("add", "➕ Add user to premium (Admin Only)"),
        BotCommand("rem", "➖ Remove from premium (Admin Only)"),
        BotCommand("stats", "📊 Get stats of the bot (Admin Only)"),
        BotCommand("freez", "🧊 Remove all expired user (Admin Only)")
    ])
 
    await message.reply("✅ Commands configured successfully!")
 
 
 
 
help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "4. **/get**\n"
        "> Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n"
        "> Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n"
        "> Download videos (Not available in v3 if you are using)\n\n"
        "7. **/adl link**\n"
        "> Download audio (Not available in v3 if you are using)\n\n"
        "8. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "9. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot\n\n"
        "11. **/stats**\n"
        "> Get bot stats\n\n"
        "12. **/plan**\n"
        "> Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "14. **/terms**\n"
        "> Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> 1. SETCHATID : To directly upload in channel or group or user's dm use it with -100[chatID]\n"
        "> 2. SETRENAME : To add custom rename tag or username of your channels\n"
        "> 3. CAPTION : To add custom caption\n"
        "> 4. REPLACEWORDS : Can be used for words in deleted set via REMOVE WORDS\n"
        "> 5. RESET : To set the things back to default\n\n"
        "> You can set CUSTOM THUMBNAIL, SESSION-based login, etc. from settings\n\n"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
     
    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")
 
     
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
     
    keyboard = InlineKeyboardMarkup([buttons])
 
     
    await message.delete()
 
     
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("hhhelp"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
 
     
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1
 
     
    await send_or_edit_help_page(client, callback_query.message, page_number)
 
     
    await callback_query.answer()
 
 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "\n\n       ~Thank You"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Mr_Mahiji")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 
 
'''@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **Premium Price**:\n\n Starting from 200 INR accepted via **__Amazon/PhonePay Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Mr_Mahiji")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)'''
 
@app.on_message(filters.command("plan"))
async def send_plan_info(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    photo_url = "https://graph.org/file/81600d79c98257f476807.jpg"
    
    # Brief caption for the photo
    brief_caption = f"**ʜᴇʏ {user}🥀,Choose Your Premium Plan!** ✨\n\n💬 **Pay to the Scanner above and after successful payment _Send Screenshot_ Plan will be activated once after screenshot received.**"
    
    # Full plan details as a separate text message
    detailed_text = """
✨ **Here are the available Plans!** ✨

🔹 **Standard Plan: 100 INR for 5 Days**
- Access exclusive tools.
- Priority support.
- Save up to 50 messages in one click.
- Early access to new features.

🔹 **Premium Plan: 200 INR for 10 Days**
- All Standard benefits.
- Extended premium period.
- Save up to 150 messages.
- Special promotions and discounts.

🔹 **Elite Plan: 500 INR for 1 Month**
- All Premium benefits.
- Best value for long-term users.
- Exclusive offers and dedicated support.
- Save up to 1000 messages.

🔹 **Customized Plan Available**
- Tailored features on request.

💡 **Special Offer**: Pick the plan that fits you best and enjoy our premium services!

💬 **Need Help?** Click "💬 Contact Now" to contact us.
"""

    # Button to contact the owner
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Mr_Mahiji")],
        ]
    )
    # Sending the detailed text message
    await client.send_message(
        chat_id=message.chat.id,
        text=detailed_text
    )
    
    # Sending the photo with the brief caption and button
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=brief_caption,
        reply_markup=reply_markup
    )
    



@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (f"**ʜᴇʏ {user}🥀,Choose Your Premium Plan!** ✨\n\n💬 **Pay to the Scanner above and after successful payment _Send Screenshot_ Plan will be activated once after screenshot received.**")
    
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Mr_Mahiji")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Mr_Mahiji")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
 
 
