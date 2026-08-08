    # main.py
    import asyncio
    import logging
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    import config
    from handlers import moderation, entertainment, chat_logic
    import database # برای مقداردهی اولیه دیتابیس

    # --- تنظیمات لاگ ---
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    async def main():
        # --- مقداردهی اولیه دیتابیس ---
        # این خط مطمئن میشه که فایل‌های دیتابیس ساخته شدن
        database.initialize_database()
        logger.info("Database initialized.")

        # --- راه‌اندازی ربات ---
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML) # یا ParseMode.MARKDOWN_V2 بسته به نیاز
        )
        dp = Dispatcher()

        # --- ثبت روترهای هندلر ---
        dp.include_router(moderation.router)
        dp.include_router(entertainment.router)
        dp.include_router(chat_logic.router)
        logger.info("Routers included.")

        # --- شروع به کار پولینگ ---
        # ربات شروع به دریافت پیام از تلگرام می‌کند
        logger.info("Bot starting polling...")
        await dp.start_polling(bot)

    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Bot stopped manually.")
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
          
