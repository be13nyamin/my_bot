# handlers/manager.py
from aiogram import Router, types
from ai.ask_ai import ask_ai
from db import get_user_status

router = Router()

@router.message()
async def handle_message(message: types.Message):
    """مدیریت پیام‌های متنی معمولی کاربر"""
    
    # اول چک می‌کنیم کاربر کی هست
    user_id = message.from_user.id
    status = get_user_status(user_id)
    
    # اگر کاربر رو نشناختیم، یعنی هنوز /start رو نزده
    if status is None:
        await message.answer("لطفاً اول دستور /start رو بفرست تا با هم آشنا بشیم! 😅")
        return

    # الان ربات داره به هوش مصنوعی وصل می‌شه، پس بهتره یه پیام "در حال پردازش" بدیم
    wait_msg = await message.answer("⌛ لطفاً صبر کن، دارم فکر می‌کنم...")
    
    # صدا زدن مغز (AI)
    response = await ask_ai(message.text)
    
    # پاک کردن پیام انتظار و ارسال جواب نهایی
    await wait_msg.delete()
    await message.answer(response)
  
