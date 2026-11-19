import os
import requests
import json
from typing import Dict, Any, List

class OpenRouterClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "").strip()
        # Free model default
        self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate_chat_response(self, messages: List[Dict[str, str]], context_data: str) -> str:
        """Calls OpenRouter with real estate context."""
        if not self.is_configured:
            return ""

        system_prompt = (
            "You are an elite, knowledgeable Real Estate AI Advisor specializing in DarGlobal international "
            "luxury projects and Wasalt Saudi property marketplace.\n"
            "Here is verified context retrieved directly from the scraped DarGlobal & Wasalt databases:\n"
            "---------------------\n"
            f"{context_data}\n"
            "---------------------\n"
            "Guidelines:\n"
            "1. Answer the user's questions accurately using the provided property knowledge.\n"
            "2. Highlight key specs such as location, pricing, brand collaborations (Trump, Pagani, Lamborghini, Missoni), and amenities.\n"
            "3. If recommending properties, format them clearly with bullet points and include direct links when available.\n"
            "4. Maintain a professional, polite, and persuasive tone suitable for luxury real estate clients."
        )

        full_messages = [{"role": "system", "content": system_prompt}] + messages

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://darglobal-wasalt-ai.app",
            "X-Title": "DarGlobal & Wasalt Real Estate AI"
        }

        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        try:
            res = requests.post(self.api_url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                print(f"OpenRouter API error {res.status_code}: {res.text}")
                return ""
        except Exception as e:
            print(f"Exception calling OpenRouter: {e}")
            return ""
