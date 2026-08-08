from aiogram import Router, types, F
from aiogram.filters import Command
from config import GROUP_LINK, CHANNEL_LINK, DEFAULT_WELCOME
from database import db

router = Router()

# دستور استارت در پیوی
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            f"سلام {message.from_user.first_name} عزیز! 👋\n\n"
            f"من ربات مدیریت گپ هستم. برای استفاده از من، من رو در گروه‌هات ادمین کن.\n\n"
            f"📢 تبلیغات گروه ما:\n{GROUP_LINK}\n\n"
            f"📢 تبلیغات کانال ما:\n{CHANNEL_LINK}"
        )
    else:
        await message.answer("من در گروه‌ها برای مدیریت حضور دارم! لطفاً من را ادمین کنید. 🛠")

# خوش‌آمدگویی به اعضای جدید در گروه
@router.chat_member()
async def welcome_member(event: types.ChatMemberUpdated):
    # فقط اگر عضو جدید اضافه شده باشه
    if event.new_chat_member.status == "member":
        chat_id = event.chat.id
        user_name = event.new_chat_member.user.first_name
        
        # چک کردن اینکه آیا این گروه در دیتابیس ما ثبت شده یا نه
        # (در مراحل بعد این بخش رو پیشرفته‌تر می‌کنیم)
        
        welcome_text = f"{DEFAULT_WELCOME}\n\nخوش اومدی {user_name} عزیز! 🎉"
        await event.bot.send_message(chat_id, welcome_text)

# دستور برای گرفتن اطلاعات (مثلاً برای تست)
@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(f"🆔 آیدی این چت: `{message.chat.id}`", parse_mode="Markdown")
  
