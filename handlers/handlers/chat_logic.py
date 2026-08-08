# handlers/chat_logic.py
import random
import re
from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.enums import ChatMemberStatus
import config
import database

router = Router()

# -----------------------------
# پاسخ به کلمات کلیدی
# -----------------------------

@router.message(F.text)
async def keyword_responder(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()
    first_name = message.from_user.first_name or "دوست عزیز"

    greetings = ["سلام", "سلااام", "salam", "درود", "hi", "hello"]
    goodbyes = ["خداحافظ", "بای", "bye", "فعلاً", "فعلا"]
    owner_words = ["مالک", "owner", "سازنده", "creator"]
    bot_words = ["آیدی سازنده", "ایدی سازنده", "id سازنده", "سازنده کیه", "ربات مال کیه", "ربات برای کیه"]
    how_are_you_words = ["خوبی", "چطوری", "خوب هستی", "حالت چطوره"]

    if any(w in text for w in greetings):
        await message.reply(random.choice([
            f"سلام {first_name} 👋",
            f"درود {first_name} 😎",
            f"سلام به روی ماهت {first_name} ✨"
        ]))
        return

    if any(w in text for w in goodbyes):
        await message.reply(random.choice([
            f"خداحافظ {first_name} 👋",
            f"فعلاً {first_name}، برگرد باز 😌",
            f"بدرود {first_name}، خیلی زود بیا دوباره"
        ]))
        return

    if any(w in text for w in owner_words):
        await message.reply(
            f"👑 مالک این ربات: `{config.OWNER_ID}`\n"
            f"بله، بالاخره یکی باید مسئول این همه هیاهو باشد."
        )
        return

    if any(w in text for w in bot_words):
        await message.reply(
            f"👤 سازنده ربات: `{config.CREATOR_ID}`\n"
            f"اگر خواستی، می‌تونم اینو با آیدی/یوزرنیم هم برات تنظیم کنم."
        )
        return

    if any(w in text for w in how_are_you_words):
        await message.reply(random.choice([
            "خوبم، مرسی از پرسیدنت 🙂",
            "عالی‌ام، چون شما اومدی 😄",
            "خوبم، امیدوارم تو هم عالی باشی ✨"
        ]))
        return


# -----------------------------
# خوشامدگویی هنگام ورود
# -----------------------------

@router.chat_member()
async def welcome_new_member(event: ChatMemberUpdated):
    if not event.new_chat_member:
        return

    # فقط ورود اعضای جدید
    if event.old_chat_member.status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED} and \
       event.new_chat_member.status == ChatMemberStatus.MEMBER:

        user = event.new_chat_member.user
        chat = event.chat

        # پیام خوشامدگویی سفارشی از دیتابیس (اگر موجود باشد)
        custom_welcome = database.get_chat_setting(chat.id, "welcome_text")
        if custom_welcome:
            text = custom_welcome.replace("{name}", user.first_name or "دوست عزیز")
        else:
            text = (
                f"🎉 خوش اومدی {user.first_name or 'دوست عزیز'} به گروه {chat.title or 'گروه'}!\n"
                f"امیدوارم اینجا خوش بگذره."
            )

        try:
            await event.answer(text)
        except Exception:
            pass


# -----------------------------
# خداحافظی هنگام خروج
# -----------------------------

@router.chat_member()
async def goodbye_member(event: ChatMemberUpdated):
    if not event.new_chat_member:
        return

    if event.old_chat_member.status in {ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED} and \
       event.new_chat_member.status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:

        user = event.old_chat_member.user
        chat = event.chat

        custom_goodbye = database.get_chat_setting(chat.id, "goodbye_text")
        if custom_goodbye:
            text = custom_goodbye.replace("{name}", user.first_name or "دوست عزیز")
        else:
            text = (
                f"👋 خداحافظ {user.first_name or 'دوست عزیز'} از {chat.title or 'گروه'}.\n"
                f"امیدواریم دوباره ببینیمت."
            )

        try:
            await event.answer(text)
        except Exception:
            pass


# -----------------------------
# پیام در پی‌وی ربات
# -----------------------------

@router.message(F.chat.type == "private")
async def private_help(message: Message):
    text = (
        "سلام! 👋\n\n"
        "من یک ربات مدیریت و سرگرمی هستم.\n"
        "قابلیت‌هام:\n"
        "• ضد لینک و ضد اسپم\n"
        "• اخطار، سکوت، بن\n"
        "• خوشامدگویی و خداحافظی\n"
        "• جوک، چالش، دانستنی، بیو\n\n"
        "اگر خواستی من رو داخل گروهت اضافه کن تا کارم رو شروع کنم.\n"
        "اگه هم بخوای، می‌تونم تنظیمات سفارشی هم بگیرم.\n"
    )
    if config.CHANNEL_USERNAME:
        text += f"\n📢 کانال: @{config.CHANNEL_USERNAME}"
    if config.GROUP_USERNAME:
        text += f"\n💬 گروه: @{config.GROUP_USERNAME}"

    await message.reply(text)


# -----------------------------
# پاسخ به منشن ربات
# -----------------------------

@router.message(F.mention)
async def bot_mention_reply(message: Message):
    try:
        await message.reply(
            "من اینجام 😎\n"
            "اگر دستور خاصی مدنظرت هست، توی پی‌وی یا گروه با من حرف بزن."
        )
    except Exception:
        pass
         
