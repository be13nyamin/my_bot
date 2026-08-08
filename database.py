import sqlite3

class Database:
    def __init__(self, db_name='bot_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # جدول تنظیمات گروه‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                anti_spam INTEGER DEFAULT 0,
                rules TEXT DEFAULT 'قوانین گروه هنوز تعیین نشده است.',
                is_active INTEGER DEFAULT 1
            )
        ''')
        self.conn.commit()

    def set_anti_spam(self, chat_id, status):
        self.cursor.execute('INSERT OR REPLACE INTO groups (chat_id, anti_spam) VALUES (?, ?)', (chat_id, status))
        self.conn.commit()

    def get_anti_spam(self, chat_id):
        self.cursor.execute('SELECT anti_spam FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def set_rules(self, chat_id, rules):
        self.cursor.execute('INSERT OR REPLACE INTO groups (chat_id, rules) VALUES (?, ?)', (chat_id, rules))
        self.conn.commit()

    def get_rules(self, chat_id):
        self.cursor.execute('SELECT rules FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "قوانینی برای این گروه تعریف نشده."

# یک نمونه از دیتابیس برای استفاده در بقیه فایل‌ها
db = Database()
