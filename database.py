import json
import os

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.data = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}, "groups": {}, "exempt_users": []}

    def _save(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_user(self, user_id):
        uid = str(user_id)
        if uid not in self.data["users"]:
            self.data["users"][uid] = {"level": 0, "warnings": {"link": 0, "spam": 0}, "alias": "Member"}
            self._save()
        return self.data["users"][uid]

    def update_user(self, user_id, key, value):
        uid = str(user_id)
        if uid in self.data["users"]:
            if isinstance(value, dict):
                self.data["users"][uid][key].update(value)
            else:
                self.data["users"][uid][key] = value
            self._save()

    def add_warning(self, user_id, warn_type):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["warnings"][warn_type] += 1
            self._save()
            return self.data["users"][uid]["warnings"][warn_type]
        return 0

    def set_level(self, user_id, level):
        self.update_user(user_id, "level", level)

    def get_level(self, user_id):
        return self.get_user(user_id)["level"]
      
