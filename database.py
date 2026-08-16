# database.py
import json
import os
from datetime import datetime

DB_FILE = "batman_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},   # آمار و سطح کاربران
            "groups": {}   # تنظیمات هر گروه
        }
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": {}, "groups": {}}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _default_group():
    return {
        "banned_words": [],
        "exempt_list": [],       # لیست معاف از اخطار
        "aliases": {},           # {user_id: {"real": "اصل", "nick": "لقب"}}
        "warnings": {},          # {user_id: count}
        "muted": [],             # کاربران ساکت
        "stats": {},             # {user_id: {"messages": n, "warns": n}}
        "locked": False
    }


def get_group(chat_id):
    db = load_db()
    key = str(chat_id)
    if key not in db["groups"]:
        db["groups"][key] = _default_group()
        save_db(db)
    return db["groups"][key]


def save_group(chat_id, data):
    db = load_db()
    db["groups"][str(chat_id)] = data
    save_db(db)


# ---------- اخطار و معاف ----------
def add_warning(chat_id, user_id):
    g = get_group(chat_id)
    uid = str(user_id)
    if uid in g["exempt_list"]:
        return 0, True  # معاف است، اخطار ثبت نشد
    g["warnings"][uid] = g["warnings"].get(uid, 0) + 1
    if "stats" not in g:
        g["stats"] = {}
    g["stats"].setdefault(uid, {"messages": 0, "warns": 0})
    g["stats"][uid]["warns"] = g["warnings"][uid]
    save_group(chat_id, g)
    return g["warnings"][uid], False


def reset_warnings(chat_id, user_id):
    g = get_group(chat_id)
    g["warnings"][str(user_id)] = 0
    save_group(chat_id, g)


# ---------- معاف ----------
def is_exempt(chat_id, user_id):
    return str(user_id) in get_group(chat_id)["exempt_list"]

def set_exempt(chat_id, user_id, state=True):
    g = get_group(chat_id)
    uid = str(user_id)
    if state and uid not in g["exempt_list"]:
        g["exempt_list"].append(uid)
    elif not state and uid in g["exempt_list"]:
        g["exempt_list"].remove(uid)
    save_group(chat_id, g)


# ---------- اصل و لقب ----------
def set_alias(chat_id, user_id, kind, value):
    g = get_group(chat_id)
    uid = str(user_id)
    g["aliases"].setdefault(uid, {"real": "", "nick": ""})
    g["aliases"][uid][kind] = value
    save_group(chat_id, g)


def get_alias(chat_id, user_id):
    return get_group(chat_id)["aliases"].get(str(user_id), {"real": "", "nick": ""})


# ---------- آمار ----------
def add_message(chat_id, user_id):
    g = get_group(chat_id)
    if "stats" not in g:
        g["stats"] = {}
    g["stats"].setdefault(str(user_id), {"messages": 0, "warns": 0})
    g["stats"][str(user_id)]["messages"] += 1
    save_group(chat_id, g)
    return g["stats"][str(user_id)]


def get_total_messages(chat_id):
    g = get_group(chat_id)
    return sum(u["messages"] for u in g.get("stats", {}).values())


# ---------- اشتراک (ویژگی تجاری) ----------
def get_user_level(user_id):
    db = load_db()
    return db["users"].get(str(user_id), {}).get("level", "FREE")

def set_user_level(user_id, level):
    db = load_db()
    db["users"].setdefault(str(user_id), {})["level"] = level
    save_db(db)

def is_premium(user_id):
    return get_user_level(user_id) in ("PRO", "GOD")

def is_admin_bot(user_id):
    return user_id in ADMIN_IDS  # از config
      
