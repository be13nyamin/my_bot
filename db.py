# db.py
import sqlite3
from config import DB_NAME

def get_connection():
    """یک اتصال تازه به دیتابیس ایجاد می‌کند."""
    return sqlite3.connect(DB_NAME)

def create_tables():
    """ساخت جداول مورد نیاز در دیتابیس (اگر وجود نداشته باشند)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # ساخت جدول کاربران
    # id: آیدی عددی تلگرام کاربر
    # is_pro: وضعیت اشتراک (1 یعنی پرو، 0 یعنی معمولی)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            is_pro INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ جداول دیتابیس با موفقیت بررسی/ساخته شدند.")

def add_user(user_id):
    """اگر کاربر جدید بود، او را در دیتابیس ثبت کن."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (user_id, is_pro) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        print(f"👤 کاربر جدید ثبت شد: {user_id}")
    except sqlite3.IntegrityError:
        # اگر کاربر از قبل وجود داشته باشد، این ارور رخ می‌دهد که یعنی کاربر قدیمی است
        pass 
    finally:
        conn.close()

def get_user_status(user_id):
    """بررسی می‌کند که آیا کاربر پرو هست یا نه."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_pro FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]  # برمی‌گرداند 1 یا 0
    return None  # یعنی کاربر اصلاً در دیتابیس نیست
