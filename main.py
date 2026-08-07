import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message

# --- تنظیمات حرفه‌ای ---
TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"

# تنظیمات لاگ (بسیار مهم برای اینکه ببینی چه اتفاقی می‌افتد)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# دیتابیس موقت در حافظه (برای سرعت بالا)
# در پروژه‌های بزرگتر از SQLite استفاده می‌کنیم
banned_users = set()

# --- توابع کمکی (Helper Functions) ---

async def is_admin(message: Message) -> bool:
    """بررسی سطح دسترسی کاربر در گروه"""
    if message.chat.type == 'private':
        return True
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['administrator', 'creator']

# --- مدیریت دستورات (Commands Handler) ---
# این بخش‌ها باید بالاتر از بقیه باشند تا اولویت داشته باشند

@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.answer(
        "🚀 **سیستم مدیریت پیشرفته فعال شد!**\n\n"
        "من آماده‌ام تا از گروه شما محافظت کنم.\n"
        "🔹 ضد لینک فعال\n"
        "🔹 سیستم بن هوشمند\n"
        "🔹 مدیریت ادمین\n\n"
        "لطفاً ربات را در گروه ادمین کنید."
    )

@dp.message(Command("ban"))
async def cmd_ban(message: Message):
    """بن کردن کاربر با ریپلای"""
    if not await is_admin(message):
        return await message.answer("❌ شما دسترسی ادمین ندارید.")

    if not message.reply_to_message:
        return await message.answer("⚠️ لطفاً برای بن کردن، روی پیام کاربر ریپلای کنید.")

    target_id = message.reply_to_message.from_user.id
    target_name = message.reply_to_message.from_user.first_name
    
    banned_users.add(target_id)
    
    try:
        await bot.ban_chat_member(message.chat.id, target_id)
        await message.answer(f"🚫 کاربر **{target_name}** ({target_id}) با موفقیت بن شد.")
        logger.info(f"User {target_id} banned by {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await message.answer("❌ خطا: من دسترسی ادمین برای بن کردن ندارم!")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "🛠 **راهنمای دستورات:**\n\n"
        "/start - فعال‌سازی ربات\n"
        "/ban - بن کردن (با ریپلای)\n"
        "/help - نمایش این راهنما"
    )
    await message.answer(help_text)

# --- پردازش پیام‌های عمومی (Middlewares Logic) ---

@dp.message()
async def main_processor(message: Message):
    """قلب تپنده ربات: این تابع تمام پیام‌ها را طبق اولویت بررسی می‌کند"""
    
    # اگر پیام متن نیست (عکس، استیکر و غیره)، کاری انجام نده
    if not message.text:
        return

    user_id = message.from_user.id
    text = message.text.lower()

    # ۱. اولویت اول: بررسی بن بودن (اگر کاربر بن بود، پیامش را پاک کن و تمام)
    if user_id in banned_users:
        try:
            await message.delete()
            logger.info(f"Deleted message from banned user: {user_id}")
        except:
            pass
        return # متوقف شدن پردازش برای این کاربر

    # ۲. اولویت دوم: بررسی لینک (فقط اگر ادمین نبود)
    links = ["http", "t.me", ".com", ".net", ".org", "www.", "https"]
    if any(link in text for link in links):
        if not await is_admin(message):
            try:
                await message.delete()
                await message.answer(f"⚠️ {message.from_user.first_name} عزیز، ارسال لینک ممنوع است!")
                logger.info(f"Link deleted from {user_id}")
            except Exception as e:
                logger.error(f"Error deleting link: {e}")
            return # متوقف شدن پردازش بعد از حذف لینک

    # ۳. اگر هیچ‌کدام از موارد بالا نبود، یعنی پیام عادی است (سلام، خداحافظ و...)
    # اینجا ربات کاری انجام نمی‌دهد و اجازه می‌دهد پیام در گروه باقی بماند.
    # اگر می‌خواهی ربات به سلام جواب بدهد، می‌توانی اینجا شرط بگذاری.
    if "سلام" in text:
        await message.answer(f"👋 سلام {message.from_user.first_name} عزیز!")

# --- شروع به کار ---

async def main():
    print("------------------------------------------")
    print("🤖 ربات پیشرفته در حال آماده‌سازی است...")
    print("📡 وضعیت اتصال به تلگرام در حال بررسی است...")
    print("------------------------------------------")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Critical Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 ربات متوقف شد.")
