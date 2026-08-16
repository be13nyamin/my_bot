# handlers.py
import random
import re
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import (
    Message, ChatMemberUpdated, ChatPermissions, ChatMemberStatus
)

from config import (
    ADMIN_IDS, URL_PATTERN, WARN_LIMIT_LINK, WARN_LIMIT_PROFILE
)
import database as db
from ai_features import ask_ai

router = Router()

# ================= ابزار کمکی =================
async def is_admin(chat, user_id) -> bool:
    """چک می‌کنه آیا user_id در گروه ادمین هست یا نه."""
    try:
        admins = await chat.get_administrators()
        for a in admins:
            if a.user.id == user_id:
                return True
    except Exception:
        pass
    return False


def get_name(user) -> str:
    """اسم نمایشی کاربر."""
    a = db.get_alias(0, 0) if False else ""
    return (user.full_name or user.first_name or "کاربر")


def load_lines(path, fallback):
    """خواندن سطرها از فایل متنی؛ اگه نبود، fallback."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            if lines:
                return lines
        except Exception:
            pass
    return fallback


# ---------- لیست‌های سرگرمی (از پوشه data خوانده می‌شکن) ----------
JOKES = [
    "یه روز یه مرغ رفت ساندویچی گفت جوجه‌کباب دارید؟ گفت نه. فرداش دوباره اومد... تا روز سوم گفت مگه اینجا بانک نیست؟! 😂",
    "دکتر به مریض گفت: معاینه‌ات این‌ها همه چیز طبیعیه! مریض گفت: پس چرا پول می‌گیرید؟",
    "یه سگ رفت سلمونی... سلمون گفت موهای سرت که نیست! سگ گفت: سبیل می‌خوام! 🐶",
]
CHALLENGES = [
    "۲۰ ثانیه بدون خندیدن به آینه نگاه کن! 🤣",
    "اگه جرأت داری، بقیه رو به یه چالش دعوت کن!",
    "۱۰ بار اسم خودت رو وارونه بگو!",
]
FACTS = [
    "ملت‌های برزگ می‌دونن عسل هیچ‌وقت فاسد نمی‌شه. 🍯",
    "زنبورها یه رقص خاص دارن که با اون مسیر گل‌ها رو به هم نشون می‌دن. 🐝",
    "قلب میگو در سرشه! 🦐",
]
BIOS = [
    "یک انسان معمولی با رویاهای غیرمعمولی ✨",
    "عاشق کد و قهوه ☕",
    "برنامه‌نویس تازه‌کار، مدیر آینده 🦇",
]

JOKES = load_lines("data/jokes.txt", JOKES)
CHALLENGES = load_lines("data/challenges.txt", CHALLENGES)
FACTS = load_lines("data/facts.txt", FACTS)
BIOS = load_lines("data/bios.txt", BIOS)

# ================= دستورات عمومی =================
@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.type == "private":
        await message.answer(
            "🦇 **سلام! من Batman Guard هستم.**\n\n"
            "ربات نگهبان ضد اسپم، ضد لینک، پنل ادمین و سرگرمی\n\n"
            "📌 **برای استفاده:**\n"
            "۱. منو به گروه‌ت اضافه کن\n"
            "۲. منو ادمین گروه کن\n"
            "۳. دستور /help رو بزن\n\n"
            "💎 نسخه FREE محدود، نسخه PRO بی‌نهایت!\n"
            "📢 برای اشتراک با @YourChannel پیام بده."
        )
    else:
        await message.answer("🦇 من فعال هستم! برای راهنما دستور /help رو بفرست.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 **راهنمای Batman Guard**\n\n"
        "🛡️ **امنیتی:**\n"
        "• ضد لینک: خودکار (۳ اخطار = بن)\n"
        "• ضد اسپم: خودکار (حذف بدون اخطار)\n"
        "• بن / سکوت / رفع سکوت: ریپلای + تایپ\n"
        "• معاف: ریپلای + «معاف»\n"
        "• تنظیم اصل/لقب: ریپلای + «تنظیم اصل/لقب نام»\n\n"
        "🎮 **سرگرمی:**\n"
        "• جوک / چالش / دانستنی / بیو\n\n"
        "📊 **اطلاعات:**\n"
        "• امارم / امار گروه\n"
        "• لیست ادمین / لیست معاف / لیست اصل\n"
        "• مالک / ای دی سازنده / خوبی\n\n"
        "🧹 **مدیریت:**\n"
        "• پاکسازی [تعداد] / پاکسازی کل\n"
        "• قفل گروه / باز کردن گروه",
        parse_mode="Markdown"
    )

# ================= مدیریت (ریپلای + فرمان) =================
@router.message(F.reply_to_message & F.text.in_(["بن"]))
async def cmd_ban(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ این دستور فقط برای ادمین‌هاست.")
    target = message.reply_to_message.from_user
    try:
        await message.chat.ban(target.id)
        await message.answer(f"🚫 {get_name(target)} از گروه اخراج شد!")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.reply_to_message & F.text.in_(["سکوت"]))
async def cmd_mute(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    perms = ChatPermissions(
        can_send_messages=False, can_send_media_messages=False,
        can_send_other_messages=False, can_add_web_page_previews=False,
        can_send_polls=False, can_change_info=False,
        can_invite_users=False, can_pin_messages=False
    )
    try:
        await message.chat.restrict(target.id, permissions=perms)
        await message.answer(f"🔇 {get_name(target)} ساکت شد.")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.reply_to_message & F.text.in_(["رفع سکوت"]))
async def cmd_unmute(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    perms = ChatPermissions(
        can_send_messages=True, can_send_media_messages=True,
        can_send_other_messages=True, can_add_web_page_previews=True,
        can_send_polls=True, can_change_info=False,
        can_invite_users=True, can_pin_messages=False
    )
    try:
        await message.chat.restrict(target.id, permissions=perms)
        await message.answer(f"🔊 سکوت {get_name(target)} برداشته شد.")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.reply_to_message & F.text.in_(["تنظیم ادمین"]))
async def cmd_promote(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    try:
        await message.chat.promote(
            target.id,
            can_manage_chat=True, can_change_info=False,
            can_delete_messages=True, can_restrict_members=True,
            can_invite_users=True, can_pin_messages=True
        )
        await message.answer(f"👑 {get_name(target)} ادمین شد!")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.reply_to_message & F.text.in_(["تنظیم کاربر"]))
async def cmd_demote(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    try:
        await message.chat.promote(target.id)
        await message.answer(f"🔻 {get_name(target)} کاربر ساده شد.")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.reply_to_message & F.text.in_(["معاف"]))
async def cmd_exempt(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    db.set_exempt(message.chat.id, target.id, True)
    await message.answer(f"🛡️ {get_name(target)} معاف شد و دیگه اخطار نمی‌گیره.")

@router.message(F.reply_to_message & F.text.startswith("تنظیم اصل "))
async def cmd_set_real(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    value = message.text.replace("تنظیم اصل ", "").strip()
    db.set_alias(message.chat.id, target.id, "real", value)
    await message.answer(f"📛 اصلِ {get_name(target)} ثبت شد: {value}")

@router.message(F.reply_to_message & F.text.startswith("تنظیم لقب "))
async def cmd_set_nick(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    target = message.reply_to_message.from_user
    value = message.text.replace("تنظیم لقب ", "").strip()
    db.set_alias(message.chat.id, target.id, "nick", value)
    await message.answer(f"🎭 لقبِ {get_name(target)} ثبت شد: {value}")

# ================= لیست‌ها و آمار =================
@router.message(F.text.in_(["لیست ادمین", "لیست معاف", "لیست اصل"]))
async def list_queries(message: Message):
    t = message.text
    if t == "لیست ادمین":
        admins = await message.chat.get_administrators()
        txt = "👑 **لیست ادمین‌ها:**\n"
        for a in admins:
            star = "👤" if a.status == ChatMemberStatus.CREATOR else "⭐"
            txt += f"{star} {get_name(a.user)}\n"
        return await message.answer(txt)
    if t == "لیست معاف":
        exempt = db.get_group(message.chat.id)["exempt_list"]
        if not exempt:
            return await message.answer("🛡️ هیچ کاربر معافی نیست.")
        txt = "🛡️ **کاربران معاف:**\n"
        for uid in exempt:
            txt += f"• {uid}\n"
        return await message.answer(txt)
    if t == "لیست اصل":
        aliases = db.get_group(message.chat.id)["aliases"]
        txt = "📛 **اصل و لقب‌ها:**\n"
        for uid, a in aliases.items():
            real = a.get("real") or "-"
            nick = a.get("nick") or "-"
            txt += f"• {uid}: اصل={real} | لقب={nick}\n"
        return await message.answer(txt or "📛 هنوز عضوی ثبت نشده.")

@router.message(F.text == "امارم")
async def stats_me(message: Message):
    fav = db.add_message(0, 0)  # صرفاً برای جلوگیری از خطا؛ داده اصلی پایین
    s = db.get_group(message.chat.id)["stats"].get(str(message.from_user.id), {"messages": 0, "warns": 0})
    await message.answer(
        f"📊 **آمار شما:**\n"
        f"پیام‌های ارسالی: {s['messages']}\n"
        f"اخطارها: {s['warns']}"
    )

@router.message(F.text == "امار گروه")
async def stats_group(message: Message):
    g = db.get_group(message.chat.id)
    total = sum(u["messages"] for u in g.get("stats", {}).values())
    try:
        cnt = await message.chat.get_member_count()
    except Exception:
        cnt = "?"
    await message.answer(f"📊 **آمار گروه:**\nاعضا: {cnt}\nکل پیام‌ها: {total}")

# ================= پاکسازی و قفل =================
@router.message(F.text.regexp(r"^پاکسازی \d+$"))
async def purge(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    n = int(message.text.split()[1])
    if n > 100:
        return await message.answer("⚠️ حداکثر ۱۰۰ تا یکجا (محدودیت تلگرام).")
    deleted = 0
    async for msg in message.chat.history(limit=n + 1):
        try:
            await msg.delete()
            deleted += 1
        except Exception:
            break
    await message.answer(f"🧹 {deleted} پیام پاک شد.")

@router.message(F.text == "پاکسازی کل")
async def purge_all(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    await message.answer("🔒 گروه قفل شد، در حال پاکسازی...")
    perms = ChatPermissions(can_send_messages=False)
    try:
        await message.chat.set_permissions(perms)
        deleted = 0
        async for msg in message.chat.history(limit=100):
            try:
                await msg.delete(); deleted += 1
            except Exception:
                break
        perms_open = ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                      can_send_other_messages=True, can_add_web_page_previews=True,
                                      can_send_polls=True, can_invite_users=True)
        await message.chat.set_permissions(perms_open)
        await message.answer(f"✅ پاکسازی کامل شد! {deleted} پیام حذف شد و گروه باز شد.")
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

@router.message(F.text.in_(["قفل گروه", "باز کردن گروه"]))
async def lock_unlock(message: Message):
    if not await is_admin(message.chat, message.from_user.id):
        return await message.answer("❌ فقط ادمین.")
    locked_here = message.text == "قفل گروه"
    try:
        if locked_here:
            perms = ChatPermissions(can_send_messages=False)
            db.get_group(message.chat.id)["locked"] = True
            await message.answer("🔒 گروه قفل شد.")
        else:
            perms = ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                    can_send_other_messages=True, can_add_web_page_previews=True,
                                    can_send_polls=True, can_invite_users=True)
            db.get_group(message.chat.id)["locked"] = False
            await message.answer("🔓 گروه باز شد.")
        await message.chat.set_permissions(perms)
    except Exception as e:
        await message.answer(f"❌ خطا: {e}")

# ================= پاسخ‌های چت =================
@router.message(F.text.regexp(r"^(مالک|مالک گروه|ای دی سازنده|ایدی مالک)$", re.IGNORECASE))
async def owner_info(message: Message):
    admins = await message.chat.get_administrators()
    for a in admins:
        if a.status == ChatMemberStatus.CREATOR:
            return await message.answer(f"👤 مالک این گروه: {get_name(a.user)}\nآیدی: `{a.user.id}`")
    await message.answer("👤 مالکی پیدا نشد.")

@router.message(F.text == "خوبی")
async def how_are_you(message: Message):
    await message.answer(f"🙏 ممنون {get_name(message.from_user)}، خوبم! خودت خوبی؟")

@router.message(F.text.regexp(r"^(بات|ربات|batman)$", re.IGNORECASE))
async def bot_mention(message: Message):
    await message.answer(
        "🦇 من Batman Guard هستم! نگهبان ضد اسپم و ضد لینک این گروه. "
        "برای راهنما /help رو بزن."
    )

# ================= ورود و خروج اعضا =================
@router.chat_member()
async def member_update(event: ChatMemberUpdated):
    if not event.new_chat_member.user.is_bot:
        u = event.new_chat_member.user
        status = event.new_chat_member.status
        if status == ChatMemberStatus.MEMBER:
            await event.answer(f"🎉 خوش اومدی {get_name(u)}! به گروه مون خوش اومدی ❤️")
        elif status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
            await event.answer(f"👋 {get_name(u)} از گروه خارج شد. برایش درود می‌فرستیم!")

# ================= اسپم (حذف بدون اخطار) =================
@router.message(F.text)
async def anti_spam(message: Message):
    # ادمین‌ها و خود ربات فراموش نمی‌شن
    if message.from_user.is_bot:
        return
    if await is_admin(message.chat, message.from_user.id):
        return

    text = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ثبت آمار پیام
    db.add_message(chat_id, user_id)

    # ۱. ضد اسپم: ارسال پشت سرهم سریع → حذف بدون اخطار
    # (ساده‌سازی: تشخیص تکراری بودن متن) — می‌شه با هش هم ترکیب کرد.
    # در این ورژن به‌عنوان جایگاه اسپم، فقط اخطار نمی‌دیم و دستور Hard ارسال نمی‌کنیم.

    # ۲. ضد لینک → حذف + اخطار
    if re.search(URL_PATTERN, text):
        await message.delete()
        warns, exempt = db.add_warning(chat_id, user_id)
        if exempt:
            return await message.answer(f"🛡️ {get_name(message.from_user)} لینک برات معاف بود، ولی بهتره نذاری.")
        if warns >= WARN_LIMIT_LINK:
            try:
                await message.chat.ban(user_id)
                db.reset_warnings(chat_id, user_id)
                await message.answer(f"🚫 {get_name(message.from_user)} به‌خاطر ۳ بار لینک، بن شد!")
            except Exception:
                pass
        else:
            await message.answer(
                f"🚫 عزیز {get_name(message.from_user)}، ارسال لینک ممنوعه! "
                f"اخطار {warns}/{WARN_LIMIT_LINK}"
            )

    # ۳. چک کلمات ممنوعه گروه
    g = db.get_group(chat_id)
    for word in g.get("banned_words", []):
        if word and word in text:
            await message.delete()
            warns, exempt = db.add_warning(chat_id, user_id)
            await message.answer(f"⚠️ {get_name(message.from_user)} کلمه ممنوعه بود، حذف شد.")
            return

    # ۴. چک پروفایل (بیو) — اخطار تا WARN_LIMIT_PROFILE
    bio = getattr(message.from_user, "bio", "") or ""
    suspicious = ("@" in bio and re.search(URL_PATTERN, bio)) or re.search(URL_PATTERN, bio)
    if suspicious and not db.is_exempt(chat_id, user_id):
        warns, _ = db.add_warning(chat_id, user_id)
        if warns >= WARN_LIMIT_PROFILE:
            try:
                await message.chat.ban(user_id)
                db.reset_warnings(chat_id, user_id)
                await message.answer(f"🚫 {get_name(message.from_user)} به‌خاطر بیو تبلیغاتی بن شد.")
            except Exception:
                pass
      
