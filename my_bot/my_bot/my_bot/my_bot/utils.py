from aiogram import types

async def get_user_name(message: types.Message):
    if message.from_user.last_name:
        return f"{message.from_user.first_name} {message.from_user.last_name}"
    return message.from_user.first_name

async def is_admin(message: types.Message, admins: list):
    member = await message.chat.get_member(message.from_user.id)
    if member.status in ['administrator', 'creator']:
        return True
    if message.from_user.id in admins:
        return True
    return False
  
