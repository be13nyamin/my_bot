import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router  # وارد کردن هندلرها

async def main():
    # تنظیمات لاگ برای اینکه بفهمیم ربات داره چه کار می‌کنه
    logging.basicConfig(level=logging.INFO)

    # ساخت شیء ربات و دیسپچر
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # وصل کردن هندلرها به دیسپچر
    dp.include_router(router)

    print("🚀 ربات با موفقیت روشن شد و آماده به کار است!")
    
    # شروع به کار ربات
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 ربات خاموش شد.")
      
