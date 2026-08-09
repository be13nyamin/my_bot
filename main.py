import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# توکن رباتت رو اینجا بذار (توصیه: از Environment Variables استفاده کن)
TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- دیتابیس ساده (بعداً باید به SQL تبدیلش کنی) ---
users_db = {}  # برای ذخیره اخطارها، وضعیت ادمین و...

@dp.message(F.text.lower().contains("سلام"))
async def welcome_user(message: Message):
    await message.reply(f"سلام {message.from_user.first_name} عزیز، چطوری؟")

@dp.message(F.text.startswith("بن") & F.reply_to_message)
async def ban_user(message: Message):
    # اینجا کد بن کردن با استفاده از bot.ban_chat_member رو اضافه می‌کنی
    await message.answer("کاربر مورد نظر با موفقیت بن شد!")

# --- بخش مدیریت لینک (ضد لینک) ---
@dp.message(F.text.contains("http") | F.text.contains("t.me"))
async def anti_link(message: Message):
    # اینجا باید منطق اخطارها رو پیاده کنی
    await message.reply("عزیز لینک ممنوعه! یک اخطار دریافت کردی.")

# --- راهنما ---
@dp.message(Command("راهنما"))
async def help_cmd(message: Message):
    help_text = """
    📜 **راهنمای ربات بنیامین:**
    1. مدیریت: بن، سکوت، رفع سکوت، معاف، پاکسازی
    2. سرگرمی: جوک، چالش، دانستنی، بیو
    3. تنظیمات: قفل گروه، باز کردن گروه
    """
    await message.answer(help_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
