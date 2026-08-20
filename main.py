# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import commands, manager
from db import create_tables

async def main():
    # ۱. آماده‌سازی دیتابیس
    create_tables()
    
    # ۲. ساخت بات و دیسپچر
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # ۳. ثبت کردن هندلرها (دست و پاها رو به ربات وصل می‌کنیم)
    dp.include_router(commands.router)
    dp.include_router(manager.router)
    
    # ۴. شروع به کار (Polling)
    print("🚀 ربات با موفقیت روشن شد!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # اجرای حلقه اصلی
    asyncio.run(main())
