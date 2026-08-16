import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

# وارد کردن ماژول‌هایی که خودمون ساختیم
from config import 8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q, 8441091476, ADMINS, ANTI_LINK, MAX_WARNINGS
from db import Database
from fun import FunModule
from ai import AIModule
from utils import get_user_name, is_admin

# تنظیمات لاگ برای اینکه اگه خطایی داد بفهمیم چی شده
logging.basicConfig(level=logging.INFO)

# مقداردهی اولیه ماژول‌ها
db = Database("my_bot/database.db")
fun = FunModule()
ai = AIModule(api_key="YOUR_KEY", enabled=False) # فعلاً غیرفعال

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- دستور /start ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_name = await get_user_name(message)
    await message.reply(f"سلام {user_name}! عزیز خوش اومدی.\nمن ربات مدیریت پیشرفته هستم. برای استفاده از دستورات، من رو در گروه‌ها ادمین کن.")

# --- دستور /joke (سرگرمی) ---
@dp.message_handler(commands=['joke'])
async def cmd_joke(message: types.Message):
    await message.reply(fun.get_joke())

# --- دستور /fact (دانستنی) ---
@dp.message_handler(commands=['fact'])
async def cmd_fact(message: types.Message):
    await message.reply(fun.get_fact())

# --- سیستم ضد لینک (Anti-Link) ---
@dp.message_handler()
async def monitor_messages(message: types.Message):
    # اگر سیستم ضد لینک فعال باشد
    if ANTI_LINK:
        # چک کردن وجود لینک در متن پیام
        if "http" in message.text or "t.me" in message.text:
            # اگر کاربر ادمین نبود، لینک رو پاک کن یا اخطار بده
            if not await is_admin(message, ADMINS):
                try:
                    await message.delete()
                    await message.answer(f"@{message.from_user.id} عزیز، ارسال لینک ممنوع است! 🚫")
                    
                    # ثبت اخطار در دیتابیس
                    new_warns = db.add_warning(message.from_user.id)
                    
                    if new_warns >= MAX_WARNINGS:
                        await message.chat.ban(message.from_user.id)
                        await message.answer(f"کاربر {message.from_user.id} به دلیل ارسال لینک بیش از حد، بن شد. 🔨")
                        db.reset_warnings(message.from_user.id)
                except Exception as e:
                    logging.error(f"Error in Anti-Link: {e}")

    # پاسخ به هوش مصنوعی اگر کاربر علامت خاصی زد (مثلاً !ai)
    if message.text and message.text.startswith("!ai "):
        prompt = message.text.replace("!ai ", "")
        response = await ai.ask_ai(prompt)
        await message.reply(response)

# --- اجرای ربات ---
async def main():
    print("--- ربات با موفقیت روشن شد! ---")
    try:
        await dp.start_polling()
    finally:
        await bot.close()
        db.close()

if __name__ == '__main__':
    asyncio.run(main())
  
