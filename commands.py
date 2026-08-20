# handlers/commands.py
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from db import add_user, get_user_status

# ایجاد یک روتر (Router) برای مدیریت دستورات این بخش
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """دستور /start که اولین برخورد کاربر با ربات است."""
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    # ۱. اول چک می‌کنیم کاربر در دیتابیس هست یا نه
    status = get_user_status(user_id)
    
    if status is None:
        # اگر نبود، ثبتش می‌کنیم
        add_user(user_id)
        msg = f"سلام {user_name}! 👋\nبه ربات هوشمن خوش اومدی. من آماده‌ام تا به سوالاتت جواب بدم."
    else:
        msg = f"خوش برگشتی {user_name}! ✨\nچطوری می‌تونم کمکت کنم؟"
    
    await message.answer(msg)

@router.message(Command("status"))
async def cmd_status(message: types.Message):
    """دستور /status برای چک کردن وضعیت اشتراک کاربر."""
    user_id = message.from_user.id
    status = get_user_status(user_id)
    
    if status == 1:
        await message.answer("💎 شم کاربر پرو هستید! از تمام امکانات لذت ببرید.")
    else:
        await message.answer("❌ شما کاربر معمولی هستید. برای دسترسی به امکانات بیشتر، پرو شوید.")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """دستور /help برای راهنمایی کاربر."""
    help_text = (
        "راهنمای استفاده از ربات:\n\n"
        "🔹 /start - شروع مجدد و خوش‌آمدگویی\n"
        " /status - مشاهده وضعیت اشتراک شما\n"
        "🔹 /hel - نمایش این راهنما\n\n"
        "همچنین می‌تونی هر سوالی داری مستقیم اینجا بنویسی تا AI برات جواب بده! 🤖"
    )
    await message.answer(help_text)
  
