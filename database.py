# database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('bot_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    # جدول کاربران
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)''')
    # جدول چت‌ها/گروه‌ها
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats 
                      (chat_id INTEGER PRIMARY KEY, title TEXT)''')
    # جدول اخطارها (برای سیستم Warning)
    cursor.execute('''CREATE TABLE IF NOT EXISTS warnings 
                      (user_id INTEGER, chat_id INTEGER, count INTEGER, 
                       PRIMARY KEY (user_id, chat_id))''')
    conn.commit()
    conn.close()

def add_user(user_id, first_name, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
                   (user_id, first_name, username))
    conn.commit()
    conn.close()

def add_chat(chat_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO chats (chat_id, title) VALUES (?, ?)", (chat_id, title))
    conn.commit()
    conn.close()
    
