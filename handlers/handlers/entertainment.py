# handlers/entertainment.py
import random
from aiogram import Router, F
from aiogram.types import Message
import database

router = Router()

# --- بخش سرگرمی ---

# دستور جوک
@router.message(F.text.lower().contains("جوک") | F.text.lower().contains("بخند"))
async def send_joke(message: Message):
    jokes = database.get_content('jokes')
    if jokes:
        await message.reply(random.choice(jokes))
    else:
        await message.reply("متاسفانه فعلا جوکی نداریم!")

# دستور چالش
@router.message(F.text.lower().contains("چالش"))
async def send_challenge(message: Message):
    challenges = database.get_content('challenges')
    if challenges:
        await message.reply(random.choice(challenges))
    else:
        await message.reply("متاسفانه فعلا چالشی نداریم!")

# دستور دانستنی
@router.message(F.text.lower().contains("دانستی") | F.text.lower().contains("اطلاعات"))
async def send_fact(message: Message):
    facts = database.get_content('facts')
    if facts:
        await message.reply(random.choice(facts))
    else:
        await message.reply("متاسفانه فعلا دانستی نداریم!")

# دستور بیو
@router.message(F.text.lower().contains("بیو"))
async def send_bio(message: Message):
    bios = database.get_content('bios')
    if bios:
        await message.reply(random.choice(bios))
    else:
        await message.reply("متاسفانه فعلا بیو نداریم!")

# --- اضافه کردن محتوا (برای ادمین‌ها) ---
# این بخش را می‌توان بعدا گسترش داد تا ادمین‌ها بتوانند محتوا را مستقیماً اضافه کنند

@router.message(F.text.lower().startswith("اضافه کن جوک"), F.from_user.id == config.OWNER_ID)
async def add_joke(message: Message):
    content = message.text[len("اضافه کن جوک"):].strip()
    if content:
        database.add_content('jokes', content)
        await message.reply("جوک با موفقیت اضافه شد! 👍")
    else:
        await message.reply("لطفاً متن جوک را بعد از دستور وارد کنید.")

@router.message(F.text.lower().startswith("اضافه کن چالش"), F.from_user.id == config.OWNER_ID)
async def add_challenge(message: Message):
    content = message.text[len("اضافه کن چالش"):].strip()
    if content:
        database.add_content('challenges', content)
        await message.reply("چالش با موفقیت اضافه شد! 👍")
    else:
        await message.reply("لطفاً متن چالش را بعد از دستور وارد کنید.")

@router.message(F.text.lower().startswith("اضافه کن دانستی"), F.from_user.id == config.OWNER_ID)
async def add_fact(message: Message):
    content = message.text[len("اضافه کن دانستی"):].strip()
    if content:
        database.add_content('facts', content)
        await message.reply("دانستی با موفقیت اضافه شد! 👍")
    else:
        await message.reply("لطفاً متن دانستنی را بعد از دستور وارد کنید.")

@router.message(F.text.lower().startswith("اضافه کن بیو"), F.from_user.id == config.OWNER_ID)
async def add_bio(message: Message):
    content = message.text[len("اضافه کن بیو"):].strip()
    if content:
        database.add_content('bios', content)
        await message.reply("بیو با موفقیت اضافه شد! 👍")
    else:
        await message.reply("لطفاً متن بیو را بعد از دستور وارد کنید.")
      
