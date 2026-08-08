# config.py

    # --- اطلاعات ربات ---
    BOT_TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"  # توکن ربات تلگرامت رو اینجا بذار

    # --- شناسه مالک و سازنده ربات (برای دسترسی‌های خاص) ---
    # این آی‌دی‌ها رو می‌تونی از @userinfobot در تلگرام بگیری
    OWNER_ID = 8441091476  # شناسه عددی مالک اصلی ربات
    CREATOR_ID = 8441091476  # شناسه عددی سازنده ربات (می‌تونه همون OWNER_ID باشه)

    # --- شناسه کانال و گروه (اختیاری) ---
    # اگر دوست داشتی، یوزرنیم کانال یا گروهت رو اینجا بذار تا در پیام‌ها نمایش داده بشه
    CHANNEL_USERNAME = "https://t.me/+AsYybSaGoUowOWQ8" # مثال: 'my_awesome_channel'
    GROUP_USERNAME = "your_group_username"   # مثال: 'https://t.me/+5S037Jw6LTI3NDhk'

    # --- تنظیمات ضد اسپم ---
    # تعداد پیام‌های تکراری پشت سر هم قبل از اخطار
    SPAM_WARNING_THRESHOLD = 5
    # تعداد اخطارهای مجاز قبل از بن شدن
    MAX_WARNINGS_BEFORE_BAN = 3

    # --- تنظیمات ضد لینک ---
    # لیستی از لینک‌هایی که نباید پاک بشن (مثلا لینک‌های خودت یا ادمین‌ها)
    ALLOWED_LINKS = [
        "t.me/your_channel_username",
        "t.me/your_group_username",
        "t.me/add_users", # برای لینک‌های اضافه کردن کاربر
    ]

    # --- تنظیمات دیگر ---
    # زمان سکوت پیش‌فرض (بر حسب ثانیه)
    DEFAULT_MUTE_DURATION = 600  # 10 دقیقه

    # Whether to enable/disable features via commands
    ENABLE_ANTI_LINK = True
    ENABLE_ANTI_SPAM = True
    ENABLE_GREETINGS = True
    ENABLE_GOODBYES = True
    ENABLE_ENTERTAINMENT = True
