# handlers.py
import re
import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import config

router = Router()

# --- ویژگی ۱: موتورِ شناسایی لینک و منشن (پیشرفته) ---
def is_restricted(text: str) -> bool:
    # شناسایی لینک‌ها و منشن‌ها
    url_pattern = r'(https?://[^\s]+|t\.me/[^\s]+|www\.[^\s]+|@[A-Za-z0-9_]+)'
    return bool(re.search(url_pattern, text))

# هندلر مدیریت (اولویت اول)
@router.message(F.text)
async def moderation_system(message: Message):
    # ربات ادمین‌ها رو پاک نمی‌کنه (این ویژگیِ ربات‌های خفنه)
    if message.from_user.id == config.OWNER_ID:
        return 

    if config.ANTI_LINK_ENABLED and is_restricted(message.text):
        try:
            await message.delete()
            # می‌تونی اینجا یه اخطار موقت هم بدی
            await message.answer(f"🚫 {message.from_user.first_name}، اینجا ارسال لینک و منشن ممنوعه!")
            return # خروج از تابع تا بقیه دستورات اجرا نشه
        except:
            pass

    # --- ویژگی ۲: پردازش دستورات خفن (اگر لینک نبود) ---
    text = message.text.lower()
    if text.startswith("/"):
        return # چون هندلرهای زیر جداگانه تعریف شدن

# --- ویژگی ۳: دستورات سرگرمی و کاربردی ---
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("سلام بنیامین! ربات در خدمت شماست. با دستورات /rules, /joke, /challenge از امکانات من استفاده کن.")

@router.message(Command("joke"))
async def cmd_joke(message: Message):
    jokes = ["چرا برنامه نویسا از نور متنفرن؟ چون همش با دارک‌مود کار می‌کنن! 😂", 
             "کدِ بدون باگ، مثلِ غذای بدون نمکه، اصلاً مزه نمیده! 🤣"]
    await message.answer(random.choice(jokes))

@router.message(Command("challenge"))
async def cmd_challenge(message: Message):
    challenges = ["یه بیت کد خفن بنویس!", "توی ۳۰ ثانیه بگو برنامه نویسی یعنی چی؟"]
    await message.answer(f"🔥 چالش: {random.choice(challenges)}")
    
