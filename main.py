# main.py

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# وارد کردن تنظیمات و دیتابیس
import config
import database

# تنظیمات لاگینگ (برای اینکه بفهمیم داخل ربات چه اتفاقی داره می‌افته و اگه خطایی بود بشه فهمید)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    """
    این تابع وقتی ربات روشن میشه (Startup) اجرا میشه.
    """
    logger.info("--- ربات در حال روشن شدن است... ---")
    
    # ۱. ایجاد جداول دیتابیس در صورت عدم وجود
    database.create_tables()
    logger.info("جداول دیتابیس با موفقیت چک/ایجاد شدند.")

    # ۲. ارسال یک پیام سلام به ادمین (اختیاری - برای اطمینان از کارکرد)
    try:
        await bot.send_message(config.OWNER_ID, "🚀 ربات با موفقیت روشن شد و آماده به کار است!")
    except Exception as e:
        logger.error(f"خطا در ارسال پیام خوش‌آمدگویی به ادمین: {e}")

    logger.info("--- ربات آماده به کار است! ---")

async def main():
    # مقداردهی اولیه بات با ویژگی‌های پیش‌فرض (مثل پشتیبانی از Markdown)
    bot = Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    
    # ایجاد دیسپچر (مدیریت‌کننده رویدادها)
    dp = Dispatcher()

    # اینجا در مراحل بعد، هندلرها (Handlers) رو اینجا اضافه می‌کنیم
    # فعلاً فقط برای اینکه ساختار درست باشه

    # اجرای ربات
    try:
        await on_startup(bot)
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"خطای بحرانی در اجرای ربات: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("ربات توسط کاربر متوقف شد.")
        
