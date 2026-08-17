import os

TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"
ADMIN_IDS = [8441091476] # آیدی عددی خودت

# تنظیمات امنیتی
URL_PATTERN = r"(https?://\S+|t\.me/\S+|@\S+)"
WARN_LIMIT_LINK = 3
WARN_LIMIT_SPAM = 5

# سطوح اشتراک
LEVELS = {"FREE": 0, "PRO": 1, "GOD": 2}

# مسیرها
DB_FILE = "database.json"
DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
  
