# ai_features.py
import httpx
from config import AI_API_KEY

async def ask_ai(prompt: str) -> str:
    """اگر کلید AI تنظیم شده باشه جواب میده، وگرنه None."""
    if not AI_API_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {AI_API_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None
      
