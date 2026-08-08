# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
import config
import database
import handlers

# تنظیمات لاگ برای اینکه توی Pydroid ببینی چی شده
logging.basicConfig(level=logging.INFO)

async def main():
    # ۱. ساخت دیتابیس
    database.init_db()
    
    # ۲. راه اندازی ربات
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    
    # ۳. وصل کردن هندلرها
    dp.include_router(handlers.router)
    
    print("--- ربات خفن بنیامین با موفقیت روشن شد! ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("ربات خاموش شد.")
        
