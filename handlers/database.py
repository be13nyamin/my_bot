# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    # جدول کاربران: شامل اخطار، وضعیت سکوت، ادمین بودن، معاف بودن، اصل و لقب
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            warnings INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            is_exempt INTEGER DEFAULT 0,
            is_muted INTEGER DEFAULT 0,
            first_name_real TEXT,
            last_name_real TEXT
        )
    ''')
    # جدول گروه‌ها: برای قفل کردن یا باز کردن کل گروه
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            is_locked INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# --- توابع مدیریت کاربر ---

def get_user(user_id):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(user_id, first_name, username):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)', 
                   (user_id, username, first_name))
    conn.commit()
    conn.close()

def update_user(user_id, column, value):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    query = f'UPDATE users SET {column} = ? WHERE user_id = ?'
    cursor.execute(query, (value, user_id))
    conn.commit()
    conn.close()

def add_warning(user_id):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET warnings = warnings + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('SELECT warnings FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return res

def get_list(column_name):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    # برای لیست ادمین یا معاف
    cursor.execute(f'SELECT first_name FROM users WHERE {column_name} = 1')
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

# --- توابع مدیریت گروه ---

def set_group_lock(group_id, status):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO groups (group_id, is_locked) VALUES (?, ?)', (group_id, status))
    conn.commit()
    conn.close()

def get_group_status(group_id):
    conn = sqlite3.connect('super_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_locked FROM groups WHERE group_id = ?', (group_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else 0
  
