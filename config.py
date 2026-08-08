# config.py

# --- General Settings ---
BOT_TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"  # توکن ربات تلگرام شما
OWNER_ID = 8441091476  # شناسه عددی مالک ربات (اگه نمی‌دونی چیه، از @userinfobot بگیر)

# --- Database Settings ---
# برای شروع، از یک دیتابیس SQLite استفاده می‌کنیم. بعداً می‌تونیم به دیتابیس‌های قوی‌تر مثل PostgreSQL مهاجرت کنیم.
DATABASE_URL = "sqlite:///data.db"  # مسیر فایل دیتابیس

# --- Bot Messages ---
GREETING_MESSAGE = """
سلام {user}! 👋
به گروه «{chat}» خوش اومدی!
لطفاً قبل از هر کاری، قوانین گروه رو بخون.
"""

FAREWELL_MESSAGE = "خداحافظ {user} 👋"

# --- Security Settings ---
ANTI_LINK_ENABLED = True  # فعال/غیرفعال کردن ضد لینک
ALLOWED_LINKS = ["yourwebsite.com", "anotherallowed.com"]  # لینک‌های مجاز (به دامنه اصلی توجه کنید)
BAD_WORDS = ["کلمه_فحش_۱", "کلمه_فحش_۲"]  # لیست کلمات نامناسب برای فیلتر

# --- Entertainment Settings ---
JOKES_ENABLED = True
TRIVIA_ENABLED = True

# --- Other Settings ---
DEFAULT_LANGUAGE = "fa"  # زبان پیش‌فرض ربات

# شما می‌تونید تنظیمات بیشتری رو اینجا اضافه کنید...
# مثلاً پیام‌های پیش‌فرض برای دستورات خاص، تنظیمات مربوط به مدیریت، و ...
