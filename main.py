# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
import config
import database
from handlers import router as main_router

logging.basicConfig(level=logging.INFO)

async def on_startup():
    database.create_tables()
    print("--- Bot is starting up... ---")
    print("--- Database initialized. ---")

async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    
    # ثبت تمام هندلرها
    dp.include_router(main_router)
    
    # آماده‌سازی دیتابیس
    await on_startup()
    
    # شروع به کار
    print("--- Bot is now ONLINE ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("--- Bot stopped. ---")
        
