import aiohttp

class AIModule:
    def __init__(self, api_key, enabled=False):
        self.api_key = api_key
        self.enabled = enabled

    async def ask_ai(self, prompt):
        if not self.enabled:
            return "سیستم هوش مصنوعی در حال حاضر غیرفعال است."
        
        # اینجا باید آدرس API مورد نظرت رو بذاری (مثل OpenAI یا غیره)
        # فعلاً یک پاسخ فرضی برمی‌گردونیم تا کد خطا نده
        return f"پاسخ هوشمند به: {prompt} (در حال اتصال به API...)"
