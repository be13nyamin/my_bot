# handlers.py
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import config
import database

router = Router()

def contains_link(text: str) -> bool:
    url_pattern = r'(https?://[^\s]+|t\.me/[^\s]+|www\.[^\s]+)'
    return re.search(url_pattern, text) is not None

@router.message(Command("start"))
async def cmd_start(message: Message):
    database.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(f"سلام {message.from_user.first_name}! ربات آماده است. 😎")

@router.message(Command("rules"))
async def cmd_rules(message: Message):
    await message.answer("قوانین: ادب و احترام! 🚫")

@router.message()
async def auto_moderator(message: Message):
    if message.text and config.ANTI_LINK_ENABLED:
        if contains_link(message.text):
            is_allowed = False
            for allowed in config.ALLOWED_LINKS:
                if allowed in message.text:
                    is_allowed = True
                    break
            if not is_allowed:
                try:
                    await message.delete()
                    await message.answer(f"⚠️ {message.from_user.first_name} عزیز، لینک ممنوع است! 🚫")
                except Exception as e:
                    print(f"Error deleting: {e}")
                    
