# ai.py
import httpx  # یک کتابخانه عالی و سریع برای ارسال درخواست‌های شبکه
from config import AI_API_URL, AI_API_KEY

async def ask_ai(user_prompt: str) -> str:
    """
    ارسال پیام کاربر به هوش مصنوعی و دریافت پاسخ.
    """
    # ساخت ساختار پیام (Payload) که هوش مصنوعی می‌فهمه
    payload = {
        "model": "gpt-3.5-turbo", # یا هر مدلی که در API خودت داری
        "messages": [
            {"role": "system", "content": "You are a helpful assistant in a Telegram Bot."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # استفاده از httpx برای ارسال درخواست به صورت ناهمگام (async)
        # این باعث می‌شه ربات در حین انتظار برای جواب AI، قفل نکنه!
        async with httpx.AsyncClient() as client:
            response = await client.post(AI_API_URL, json=payload, headers=headers, timeout=30.0)
            
            # اگر پاسخ موفقیت‌آمیز بود (کد 200)
            if response.status_code == 200:
                data = response.json()
                # استخراج متن پاسخ از ساختار پیچیده JSON
                return data['choices'][0]['message']['content']
            else:
                return f"❌ ارور از سمت هوش مصنوعی: {response.status_code} - {response.text}"
                
    except Exception as e:
        return f"❌ خطای سیستمی در ارتباط با AI: {str(e)}"
      
