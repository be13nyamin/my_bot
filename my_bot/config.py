import os

# --- تنظیمات اصلی ربات ---
BOT_TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"  # توکن خودت رو اینجا بذار
OWNER_ID = 8441091476               # آیدی عددی خودت (مالک)
ADMINS = [OWNER_ID, 987654321]     # لیست آیدی ادمین‌ها

# --- تنظیمات هوش مصنوعی (AI) ---
AI_API_KEY = "YOUR_AI_API_KEY"    # اگر داری، اینجا بذار
AI_ENABLED = False                 # اگر نداری، False بذار تا ربات خطا نده

# --- تنظیمات دیتابیس ---
DB_PATH = "my_bot/database.db"

# --- تنظیمات مدیریت گروه ---
ANTI_LINK = True                   # فعال/غیرفعال کردن ضد لینک
MAX_WARNINGS = 3                   # تعداد اخطار قبل از بن شدن
SILENCE_DURATION = 3600             # مدت زمان سکوت گروه (به ثانیه)

# --- تنظیمات سرگرمی ---
USE_FUN_MODULE = True
