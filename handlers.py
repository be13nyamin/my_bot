# handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import config
import database

# ایجاد یک روتر برای مدیریت پیام‌ها
router = Router()

# دستور شروع (start/)
@router.message(Command("start"))
async def cmd_start(message: Message):
    # ذخیره اطلاعات کاربر در دیتابیس
    database.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    
    await message.answer(f"سلام {message.from_user.first_name} عزیز! به ربات من خوش اومدی. من اینجا هستم تا با قدرت و هوشمندی بهت کمک کنم. 😉")

# نمونه پاسخ به پیام‌های متنی ساده
@router.message(F.text == "سلام")
async def cmd_hello(message: Message):
    await message.answer("سلام به روی ماهت! چطور می‌تونم امروز کمکت کنم؟")

# دستور دریافت قوانین (مثال)
@router.message(Command("rules"))
async def cmd_rules(message: Message):
    await message.answer("قوانین ساده‌ست: احترام، ادب و خفن بودن! 😎")
    
