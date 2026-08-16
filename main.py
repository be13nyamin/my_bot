# main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
import handlers

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    print("🦇 Batman Guard Pro is RUNNING...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 خدافظ بنیامین!")
      
