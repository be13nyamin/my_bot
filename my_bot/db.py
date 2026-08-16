import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # جدول برای مدیریت اخطارها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
        ''')
        # جدول برای وضعیت سکوت (Mute)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS silence (
                chat_id INTEGER PRIMARY KEY,
                until_timestamp INTEGER
            )
        ''')
        # جدول برای آمار
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                chat_id INTEGER PRIMARY KEY,
                total_messages INTEGER DEFAULT 0,
                member_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_warning(self, user_id):
        self.cursor.execute('INSERT OR IGNORE INTO warnings (user_id, count) VALUES (?, 0)', (user_id,))
        self.cursor.execute('UPDATE warnings SET count = count + 1 WHERE user_id = ?', (user_id,))
        self.conn.commit()
        self.cursor.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]

    def get_warnings(self, user_id):
        self.cursor.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else 0

    def reset_warnings(self, user_id):
        self.cursor.execute('DELETE FROM warnings WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def set_silence(self, chat_id, until):
        self.cursor.execute('INSERT OR REPLACE INTO silence (chat_id, until_timestamp) VALUES (?, ?)', (chat_id, until))
        self.conn.commit()

    def is_silenced(self, chat_id):
        import time
        self.cursor.execute('SELECT until_timestamp FROM silence WHERE chat_id = ?', (chat_id,))
        res = self.cursor.fetchone()
        if res and res[0] > time.time():
            return True
        return False

    def close(self):
        self.conn.close()
      
