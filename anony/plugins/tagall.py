import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

from anony import app

TAGALL_ACTIVE = {}

@app.on_message(filters.command(["tagall", "utag"]) & filters.group)
async def tag_single_members(client, message):
    chat_id = message.chat.id
    
    # Check if user is admin
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ Sirf admins hi tagall command use kar sakte hain!")

    if TAGALL_ACTIVE.get(chat_id):
        return await message.reply_text("⚠️ Tagging already chal rahi hai. Rokne ke liye `/cancel` use karein.")

    TAGALL_ACTIVE[chat_id] = True
    custom_text = message.text.split(None, 1)[1] if len(message.command) > 1 else "Hello!"
    
    await message.reply_text("📢 Single tagging shuru ho gayi hai...")

    try:
        async for member in client.get_chat_members(chat_id):
            if not TAGALL_ACTIVE.get(chat_id):
                break
            if member.user.is_bot or member.user.is_deleted:
                continue

            mention_text = f"{member.user.mention} {custom_text}"
            try:
                await client.send_message(chat_id, mention_text)
                await asyncio.sleep(2)  # Har tag ke beech 2 second ka gap taaki bot freeze na ho
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                continue

    except Exception as e:
        await message.reply_text(f"Error: {e}")
    finally:
        TAGALL_ACTIVE[chat_id] = False
        await message.reply_text("✅ Tagging complete!")

@app.on_message(filters.command(["cancel", "stopmention"]) & filters.group)
async def cancel_tagall(client, message):
    chat_id = message.chat.id
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ Sirf admins cancel kar sakte hain!")

    if TAGALL_ACTIVE.get(chat_id):
        TAGALL_ACTIVE[chat_id] = False
        await message.reply_text("🛑 Tagging rok di gayi hai.")
    else:
        await message.reply_text("Koi active tagging process nahi chal raha hai.")
      
