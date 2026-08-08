# database.py

import sqlite3
from config import DATABASE_URL

# --- Database Connection ---
def get_db_connection():
    """
    اتصال به دیتابیس SQLite و بازگرداندن کانکشن.
    """
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # برای اینکه نتایج به صورت دیکشنری برگردونده بشن
    return conn

# --- Table Creation ---
def create_tables():
    """
    ایجاد جداول مورد نیاز در دیتابیس در صورت عدم وجود.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # جدول کاربران (برای ذخیره اطلاعات پایه کاربرانی که با ربات تعامل داشتن)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT
        )
    """)

    # جدول گروه‌ها (برای ذخیره اطلاعات گروه‌هایی که ربات در اونها عضو هست)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            username TEXT
        )
    """)

    # جدول قوانین گروه (برای ذخیره قوانین هر گروه)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            chat_id INTEGER,
            rule_text TEXT,
            rule_number INTEGER,
            PRIMARY KEY (chat_id, rule_number),
            FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE
        )
    """)

    # جدول بن شده‌ها (برای ذخیره کاربرانی که در گروه بن شدن)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            ban_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_id INTEGER,
            banned_by INTEGER, -- ادمینی که بن کرده
            reason TEXT,
            ban_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # جدول هشدارها (برای ذخیره هشدارهایی که به کاربران داده شده)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            warning_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_id INTEGER,
            warned_by INTEGER, -- ادمینی که هشدار داده
            reason TEXT,
            warning_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # می‌تونیم جداول دیگه‌ای هم برای آمار، چالش‌ها، جوک‌ها و ... اضافه کنیم.

    conn.commit()
    conn.close()

# --- Basic Data Operations (Example) ---
# توابع بیشتری برای اضافه کردن، حذف کردن و گرفتن اطلاعات از جداول اضافه خواهیم کرد.

def add_user(user_id: int, first_name: str, username: str | None):
    """
    اضافه کردن کاربر جدید به جدول users.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
                       (user_id, first_name, username))
        conn.commit()
    except sqlite3.IntegrityError:
        # کاربر قبلاً وجود داشته، کاری انجام نمی‌دهیم
        pass
    finally:
        conn.close()

def add_chat(chat_id: int, title: str, username: str | None):
    """
    اضافه کردن گروه جدید به جدول chats.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO chats (chat_id, title, username) VALUES (?, ?, ?)",
                       (chat_id, title, username))
        conn.commit()
    except sqlite3.IntegrityError:
        # گروه قبلاً وجود داشته، کاری انجام نمی‌دهیم
        pass
    finally:
        conn.close()

# --- Initialize Database ---
# این تابع رو موقع اجرای اولیه ربات صدا می‌زنیم تا جداول رو بسازه.
# create_tables()
