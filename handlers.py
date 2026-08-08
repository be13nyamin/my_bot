# handlers.py
import re
import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import config
import database

router = Router()

# --- بخش اول: ابزارهای کمکی (Utilities) ---

def contains_link_or_mention(text: str) -> bool:
    """تشخیص لینک و همچنین منشن کردن با @"""
    # الگوی تشخیص لینک (http, https, t.me, www)
    url_pattern = r'(https?://[^\s]+|t\.me/[^\s]+|www\.[^\s]+)'
    # الگوی تشخیص منشن (مثل @username)
    mention_pattern = r'@\w+'
    
    has_url = re.search(url_pattern, text) is not None
    has_mention = re.search(mention_pattern, text) is not None
    
    return has_url or has_mention

# --- بخش دوم: مدیریت خودکار (Anti-Link & Anti-Mention) ---

@router.message()
async def auto_moderator(message: Message):
    # اگر پیام حاوی لینک یا منشن بود
    if message.text and config.ANTI_LINK_ENABLED:
        if contains_link_or_mention(message.text):
            # چک کردن اینکه آیا لینک جزو لیست سفید (مجاز) هست یا نه
            is_allowed = False
            for allowed in config.ALLOWED_LINKS:
                if allowed in message.text:
                    is_allowed = True
                    break
            
            if not is_allowed:
                try:
                    # حذف پیام
                    await message.delete()
                    # ارسال اخطار
                    await message.answer(f"⚠️ {message.from_user.first_name} عزیز، ارسال لینک یا منشن ممنوع است! 🚫")
                except Exception as e:
                    # اگر ربات ادمین نباشد یا دسترسی حذف نداشته باشد، اینجا چاپ می‌شود
                    print(f"Moderation Error: {e}")

# --- بخش سوم: دستورات اصلی (Commands) ---

@router.message(Command("start"))
async def cmd_start(message: Message):
    database.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(f"سلام {message.from_user.first_name}! من ربات مدیریت پیشرفته هستم. 😎\n\nدستورات من:\n/rules - قوانین\n/joke - جوک\n/challenge - چالش")

@router.message(Command("rules"))
async def cmd_rules(message: Message):
    await message.answer("📜 **قوانین گروه:**\n1. احترام به اعضا\n2. ممنوعیت لینک و منشن غیرمجاز\n3. رعایت ادب")

# --- بخش چهارم: ویژگی‌های سرگرمی (Entertainment) ---

@router.message(Command("joke"))
async def cmd_joke(message: Message):
    jokes = [
        "یه روز یه مرده میره دکتر، میگه دکتر من هر جا رو دست می‌زنم درد می‌کنه، دست می‌زنم به سرم درد می‌کنه، دست می‌زنم به پام درد می‌کنه! دکتر میگه: آخه انگشتت شکسته! 😂",
        "یه بنده خدایی میره رستوران، میگه من یه غذا می‌خوام که خیلی سریع باشه. گارسون میگه: بفرمایید، این هم همون غذایی که نخواستید ولی خیلی سریع اومد! 🤣",
        "چرا ماهی‌ها در دریا زندگی می‌کنند؟ چون اگر بیاید بیرون، خیس می‌شود! 🐟😂"
    ]
    await message.answer(random.choice(jokes))

@router.message(Command("challenge"))
async def cmd_challenge(message: Message):
    challenges = [
        "تلاش کن ۱ دقیقه بدون پلک زدن به صفحه نگاه کنی! 👀",
        "تلاش کن نام خودت را با چشم بسته بنویسی! ✍️",
        "تلاش کن ۳۰ ثانیه بدون حرف زدن فقط با حرکات دست صحبت کنی! 🙊"
    ]
    await message.answer(f"🎯 **چالش جدید:**\n\n{random.choice(challenges)}")
    
