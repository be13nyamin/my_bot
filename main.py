import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import random

# توکن رباتت رو اینجا بذار
TOKEN = "8642906741:AAGc-cXICORZ59kmIfSt3gA42BCDyASpq1Q"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# لیست‌های سرگرمی (بنیامین، این‌ها رو می‌تونی هر چقدر بخوای زیاد کنی)
JOKES = ["جوک ۱", "جوک ۲", "جوک ۳"]
CHALLENGES = ["چالش ۱", "چالش ۲", "چالش ۳"]
FACTS = ["دانستنی ۱", "دانستنی ۲", "دانستنی ۳"]

# سیستم ساده ضد لینک (ساده و سریع)
@dp.message(F.text.contains("http") | F.text.contains("www") | F.text.contains(".com"))
async def anti_link(message: Message):
    await message.delete()
    await message.answer(f"کاربر {message.from_user.first_name}، ارسال لینک ممنوعه!")

# پاسخ‌های خودکار
@dp.message(F.text.lower() == "سلام")
async def hello(message: Message):
    await message.answer(f"سلام بنیامین‌دوست! چطوری {message.from_user.first_name}؟")

# دستور راهنما
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("لیست دستورات:\n/joke - یک جوک\n/fact - یک دانستنی\n/challenge - یک چالش")

# دستور سرگرمی
@dp.message(Command("joke"))
async def joke_cmd(message: Message):
    await message.answer(random.choice(JOKES))

@dp.message(Command("fact"))
async def fact_cmd(message: Message):
    await message.answer(random.choice(FACTS))

# شروع به کار ربات
async def main():
    print("ربات روشن شد...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
