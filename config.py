# config.py
# این فایل حاوی اطلاعات حساس و تنظیمات اصلی ربات است.

# اطلاعات ربات تلگرام
import os
from dotenv import load_dotenv

# اگر فایل .env در مسیر فعلی نیست، مسیر درست را مشخص کنید.
# به عنوان مثال: load_dotenv(dotenv_path='/path/to/your/.env')
load_dotenv() 

# خواندن توکن از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

# بررسی اینکه آیا توکن با موفقیت خوانده شده است یا نه
if not BOT_TOKEN:
    # اینجا می‌توانید یک پیام خطا نمایش دهید یا برنامه را متوقف کنید
    raise ValueError("توکن ربات پیدا نشد! لطفاً فایل .env را بررسی کنید و مطمئن شوید که BOT_TOKEN تعریف شده است.")

# حالا می‌توانید از BOT_TOKEN در بقیه برنامه استفاده کنید

ADMIN_ID = 8441091476  # آیدی عددی خودت رو اینجا بنویس

# تنظیمات دیتابیس
DB_NAME = "bot_database.db"

# تنظیمات هوش مصنوعی (AI)
AI_API_URL = "https://t.me/+AsYybSaGoUowOWQ8"
AI_API_KEY = AI_API_KEY = os.getenv("AI_API_KEY")

# تنظیمات اشتراک و قیمت‌گذاری (برای آینده)
PRO_SUBSCRIPTION_PRICE = 80000  # مثلاً ۸۰ هزار تومان
