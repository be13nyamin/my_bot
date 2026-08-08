# main.py
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
import config
import database
from handlers import router as main_router

# تنظیمات لاگ برای اینکه اگر اروری داد، دقیقاً توی Pydroid بتونیم ببینیم چی شده
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def on_startup():
    """اجرا هنگام شروع به کار ربات"""
    try:
        # ایجاد جداول دیتابیس اگر وجود ندارند
        database.create_tables()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Error during database initialization: {e}")

async def main():
    # ایجاد شیء ربات با توکن تنظیم شده در config.py
    bot = Bot(token=config.TOKEN)
    
    # ایجاد دیسپچر (مدیریت‌کننده اصلی رویدادها)
    dp = Dispatcher()
    
    # --- بخش حیاتی: ثبت تمام هندلرها ---
    # این خط باعث میشه تمام کدهای داخل handlers.py (مثل ضد لینک و دستورات) به ربات اضافه بشه
    dp.include_router(main_router)
    logger.info("✅ All routers have been included.")
    
    # اجرای عملیات شروع (ایجاد دیتابیس)
    await on_startup()
    
    # شروع دریافت پیام‌ها (Polling)
    logger.info("🚀 Bot is starting polling...")
    try:
        awai dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Error in polling: {e}")
    finally:
        # بستن اتصال ربات در صورت توقف
        await bot.session.close()

if __name__ == "__main__":
    # استفاده از ساختار استاندارد برای اجرای برنامه‌های Async در پایتون
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Bot stopped by user.")
    except Exception as e:
        logge.critical(f"💥 Fatal error: {e}")
        
