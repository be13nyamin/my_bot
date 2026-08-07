import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web  # اضافه شده برای گول زدن رندر

# --- تنظیمات حرفه‌ای ---
# حتماً از Environment Variable استفاده کن یا توکن جدید رو اینجا بذار
TOKEN = os.getenv("BOT_TOKEN", "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

banned_users = set()

# --- توابع کمکی ---
async def is_admin(message: Message) -> bool:
    if message.chat.type == 'private':
        return True
    try:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ['administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

# --- مدیریت دستورات ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 **سیستم مدیریت پیشرفته فعال شد!**\n\nلطفاً ربات را در گروه ادمین کنید.")

@dp.message(Command("ban"))
async def cmd_ban(message: Message):
    if not await is_admin(message):
        return await message.answer("❌ شما دسترسی ادمین ندارید.")
    if not message.reply_to_message:
        return await message.answer("⚠️ لطفاً روی پیام کاربر ریپلای کنید.")

    target_id = message.reply_to_message.from_user.id
    target_name = message.reply_to_message.from_user.first_name
    banned_users.add(target_id)
    
    try:
        await bot.ban_chat_member(message.chat.id, target_id)
        await message.answer(f"🚫 کاربر **{target_name}** بن شد.")
    except Exception as e:
        await message.answer("❌ خطا در بن کردن!")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("🛠 **راهنمای دستورات:**\n/start - شروع\n/ban - بن کردن\n/help - راهنما")

# --- پردازش پیام‌ها ---
@dp.message()
async def main_processor(message: Message):
    if not message.text:
        return

    user_id = message.from_user.id
    text = message.text.lower()

    if user_id in banned_users:
        try:
            await message.delete()
        except:
            pass
        return

    links = ["http", "t.me", ".com", ".net", ".org", "www.", "https"]
    if any(link in text for link in links):
        if not await is_admin(message):
            try:
                await message.delete()
                await message.answer(f"⚠️ {message.from_user.first_name} عزیز، لینک ممنوع است!")
            except:
                pass
            return

    if "سلام" in text:
        await message.answer(f"👋 سلام {message.from_user.first_name} عزیز!")

# --- بخش مخصوص رندر (گول زدن پورت) ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    logger.info("🌐 Web server started for Render compatibility!")

# --- شروع به کار ---
async def main():
    print("------------------------------------------")
    print("🤖 ربات در حال آماده‌سازی است...")
    print("------------------------------------------")
    
    # اول سرور رو راه می‌ندازیم که رندر خوشحال بشه
    await start_web_server()
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Critical Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
                        
