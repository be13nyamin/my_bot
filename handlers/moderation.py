# handlers/moderation.py
import re
from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
from aiogram.utils.markdown import hide_link
import config
import database

router = Router()

# --- ابزارهای کمکی برای مدیریت ---
def is_owner(user_id):
    return user_id == config.OWNER_ID

def get_target_message(message: Message):
    """اگر پیام ریپلای بود، پیام هدف رو برمی‌گردونه."""
    if message.reply_to_message:
        return message.reply_to_message
    return None

# --- بخش اول: مدیریت عمومی (Anti-Link, Anti-Spam) ---

@router.message(F.text, ~F.from_user.id.in_({config.OWNER_ID})) # پیام‌های متنی غیر از ادمین
async def general_moderation(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # بررسی قفل بودن گروه
    if database.get_group_status(chat_id) == 1:
        # اگر گروه قفل است، فقط ادمین‌ها و معاف‌ها می‌توانند پیام دهند
        user_data = database.get_user(user_id)
        if not (user_data and (user_data[1] == 1 or user_data[2] == 1)): # is_admin or is_exempt
            try:
                await message.delete()
                return 
            except:
                pass # اگر ربات دسترسی نداشت، خطا ندهد

    # 1. ضد لینک (با امکان استثنا)
    if config.ANTI_LINK_ENABLED and not (database.get_user(user_id) and database.get_user(user_id)[2] == 1): # اگر کاربر معاف نیست
        if re.search(r'(https?://|t\.me/|www\.)', message.text):
            # بررسی لینک‌های مجاز
            is_allowed = False
            for allowed in config.ALLOWED_LINKS:
                if allowed in message.text:
                    is_allowed = True
                    break
            if not is_allowed:
                warnings = database.add_warning(user_id)
                await message.delete()
                msg = await message.answer(f"⚠️ {message.from_user.first_name}، ارسال لینک ممنوع است! این اخطار شما شماره {warnings} از {config.MAX_WARNINGS} است.")
                if warnings >= config.MAX_WARNINGS:
                    try:
                        await message.chat.ban(user_id)
                        await msg.edit_text(f"🚫 {message.from_user.first_name} به دلیل ارسال مکرر لینک، از گروه اخراج شد.")
                    except:
                        await msg.edit_text("🚫 امکان اخراج کاربر وجود ندارد (احتمالا ربات دسترسی کافی ندارد).")
                return

    # 2. اسپم (بدون ثبت اخطار)
    # اگر پیام فقط حاوی یک کاراکتر تکراری بود (مثل "ااااا" یا "؟؟؟؟؟")
    if re.fullmatch(r'([a-zA-Z0-9\W])\1+', message.text) and len(message.text) > 5:
        await message.delete()
        await message.answer(f"🚫 {message.from_user.first_name}، ارسال پیام‌های اسپم ممنوع است!")
        return
        
# --- بخش دوم: دستورات مدیریت (با ریپلای) ---

@router.message(Command("بن"), F.reply_to_message)
async def cmd_ban(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    chat_id = message.chat.id

    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # اگر مالک یا ادمین است
        if target_user_id == config.OWNER_ID or target_user_id == message.from_user.id:
            await message.reply("نمی‌توانم خودم یا مالک را بن کنم.")
            return
        
        user_data = database.get_user(target_user_id)
        if user_data and user_data[1] == 1: # اگر هدف ادمین است
             await message.reply("نمی‌توانم ادمین‌ها را بن کنم.")
             return
             
        try:
            await message.chat.ban(target_user_id)
            await message.reply(f"کاربر {target_message.from_user.first_name} با موفقیت بن شد. 🔨")
        except Exception as e:
            await message.reply(f"خطا در بن کردن کاربر: {e}")
            
@router.message(Command("سکوت"), F.reply_to_message)
async def cmd_mute(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    chat_id = message.chat.id
    
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # اگر مالک یا ادمین است
        if target_user_id == config.OWNER_ID or target_user_id == message.from_user.id:
            await message.reply("نمی‌توانم خودم یا مالک را سکوت کنم.")
            return

        user_data = database.get_user(target_user_id)
        if user_data and user_data[1] == 1: # اگر هدف ادمین است
             await message.reply("نمی‌توانم ادمین‌ها را سکوت کنم.")
             return
             
        if user_data and user_data[5] == 1: # اگر قبلا سکوت شده
            await message.reply("این کاربر قبلا سکوت شده است.")
            return

        try:
            await message.chat.restrict(chat_id=chat_id, user_id=target_user_id, permissions=ChatPermissions(can_send_messages=False))
            database.update_user(target_user_id, 'is_muted', 1)
            await message.reply(f"کاربر {target_message.from_user.first_name} با موفقیت سکوت شد. 🤐")
        except Exception as e:
            await message.reply(f"خطا در سکوت کردن کاربر: {e}")

@router.message(Command("رفع سکوت"), F.reply_to_message)
async def cmd_unmute(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    chat_id = message.chat.id
    
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # اگر مالک یا ادمین است
        user_data = database.get_user(target_user_id)
        if not (user_data and user_data[5] == 1): # اگر سکوت نیست
            await message.reply("این کاربر در حال حاضر سکوت نیست.")
            return

        try:
            await message.chat.restrict(chat_id=chat_id, user_id=target_user_id, permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ))
            database.update_user(target_user_id, 'is_muted', 0)
            await message.reply(f"سکوت کاربر {target_message.from_user.first_name} برداشته شد. ✅")
        except Exception as e:
            await message.reply(f"خطا در رفع سکوت کاربر: {e}")

@router.message(Command("ارتقا"), F.reply_to_message)
async def cmd_promote(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id):
        if target_user_id == config.OWNER_ID:
            await message.reply("این کاربر از قبل ادمین ارشد است.")
            return
        
        database.update_user(target_user_id, 'is_admin', 1)
        await message.reply(f"{target_message.from_user.first_name} به مقام ادمین ارتقا یافت! 👑")
    else:
        await message.reply("فقط مالک ربات می‌تواند کاربران را ارتقا دهد.")

@router.message(Command("تنظیم ادمین"), F.reply_to_message)
async def cmd_set_admin(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id):
        if target_user_id == config.OWNER_ID:
            await message.reply("این کاربر از قبل ادمین ارشد است.")
            return
        
        database.update_user(target_user_id, 'is_admin', 1)
        await message.reply(f"کاربر {target_message.from_user.first_name} به عنوان ادمین تنظیم شد. 🛠️")
    else:
        await message.reply("فقط مالک ربات می‌تواند کاربران را به عنوان ادمین تنظیم کند.")

@router.message(Command("تنظیم کاربر ساده"), F.reply_to_message)
async def cmd_set_simple_user(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id):
        if target_user_id == config.OWNER_ID:
            await message.reply("این کاربر مالک اصلی است و نمی‌تواند به کاربر ساده تبدیل شود.")
            return
        
        database.update_user(target_user_id, 'is_admin', 0)
        await message.reply(f"کاربر {target_message.from_user.first_name} به کاربر عادی تبدیل شد. 🚶")
    else:
        await message.reply("فقط مالک ربات می‌تواند کاربران را به کاربر عادی تبدیل کند.")

@router.message(Command("معاف"), F.reply_to_message)
async def cmd_exempt(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        if target_user_id == config.OWNER_ID:
            await message.reply("مالک اصلی همیشه معاف است.")
            return
            
        database.update_user(target_user_id, 'is_exempt', 1)
        await message.reply(f"کاربر {target_message.from_user.first_name} از دریافت اخطار معاف شد. ✅")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند کسی را معاف کنند.")

@router.message(Command("تنظیم اصل"), F.reply_to_message)
async def cmd_set_real_name(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("لطفا نام اصلی را بعد از دستور وارد کنید. مثال: `/تنظیم اصل نام اصلی شما`")
        return
        
    real_name = parts[1]
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        database.update_user(target_user_id, 'first_name_real', real_name)
        await message.reply(f"نام اصلی {target_message.from_user.first_name} به «{real_name}» تنظیم شد.")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند نام اصلی را تنظیم کنند.")

@router.message(Command("تنظیم لقب"), F.reply_to_message)
async def cmd_set_nickname(message: Message):
    target_message = get_target_message(message)
    if not target_message: return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("لطفا لقب را بعد از دستور وارد کنید. مثال: `/تنظیم لقب لقب شما`")
        return
        
    nickname = parts[1]
    target_user_id = target_message.from_user.id
    
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        database.update_user(target_user_id, 'last_name_real', nickname)
        await message.reply(f"لقب {target_message.from_user.first_name} به «{nickname}» تنظیم شد.")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند لقب را تنظیم کنند.")

# --- بخش سوم: نمایش لیست‌ها ---

@router.message(Command("لیست ادمین"))
async def cmd_list_admins(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        admins = database.get_list('is_admin')
        if not admins:
            await message.reply("هنوز کاربری به عنوان ادمین تنظیم نشده است.")
        else:
            admin_list = "\n".join([f"- {admin}" for admin in admins])
            await message.reply(f"👑 **لیست ادمین‌ها:**\n{admin_list}")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند لیست ادمین‌ها را ببینند.")

@router.message(Command("لیست معاف"))
async def cmd_list_exempt(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        exempts = database.get_list('is_exempt')
        if not exempts:
            await message.reply("هیچ کاربری معاف نشده است.")
        else:
            exempt_list = "\n".join([f"- {exmp}" for exmp in exempts])
            await message.reply(f"🛡️ **لیست کاربران معاف:**\n{exempt_list}")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند لیست کاربران معاف را ببینند.")

# --- بخش چهارم: پاکسازی و قفل گروه ---

@router.message(Command("پاکسازی"))
async def cmd_purge(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("لطفا تعداد پیام‌های مورد نظر برای پاکسازی را مشخص کنید. مثال: `/پاکسازی 50`")
            return
            
        try:
            limit = int(parts[1])
            if limit <= 0:
                await message.reply("تعداد باید مثبت باشد.")
                return
            
            # پاکسازی پیام‌های اخیر
            deleted = await message.chat.purge(limit=limit)
            await message.reply(f"تعداد {len(deleted)} پیام پاک شد.")
            
        except ValueError:
            await message.reply("لطفا یک عدد معتبر برای تعداد وارد کنید.")
        except Exception as e:
            await message.reply(f"خطا در پاکسازی: {e}")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند پیام‌ها را پاکسازی کنند.")

@router.message(Command("پاکسازی کل"))
async def cmd_purge_all(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        try:
            # قفل کردن گروه قبل از پاکسازی کامل
            database.set_group_lock(message.chat.id, 1)
            await message.chat.restrict(chat_id=message.chat.id, user_id=message.from_user.id, permissions=ChatPermissions(can_send_messages=True)) # موقتا دسترسی مالک رو باز نگه میداره
            
            await message.reply("در حال پاکسازی کامل گروه... این عملیات ممکن است کمی طول بکشد.")
            await message.chat.purge(limit="max") # پاکسازی تمام پیام‌ها
            
            # باز کردن گروه بعد از اتمام پاکسازی
            database.set_group_lock(message.chat.id, 0)
            await message.chat.restrict(chat_id=message.chat.id, user_id=message.from_user.id, permissions=ChatPermissions(
                can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True,
                can_add_web_page_previews=True, can_change_info=False, can_invite_users=False, can_pin_messages=False
            ))
            await message.reply("پاکسازی کامل گروه با موفقیت انجام شد و گروه باز شد.")
            
        except Exception as e:
            await message.reply(f"خطا در پاکسازی کامل گروه: {e}")
            database.set_group_lock(message.chat.id, 0) # در صورت خطا، گروه را باز کند
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند گروه را به طور کامل پاکسازی کنند.")

@router.message(Command("قفل گروه"))
async def cmd_lock_group(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        database.set_group_lock(message.chat.id, 1)
        await message.reply("گروه با موفقیت قفل شد. ارسال پیام برای کاربران عادی ممنوع است.")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند گروه را قفل کنند.")

@router.message(Command("باز کردن گروه"))
async def cmd_unlock_group(message: Message):
    if is_owner(message.from_user.id) or database.get_user(message.from_user.id)[1] == 1: # مالک یا ادمین
        database.set_group_lock(message.chat.id, 0)
        await message.reply("گروه با موفقیت باز شد. ارسال پیام برای همه آزاد است.")
    else:
        await message.reply("فقط ادمین‌ها و مالک می‌توانند گروه را باز کنند.")
