import os
import json
import time
import re
import base64
import requests
import tiktoken
from dotenv import load_dotenv

load_dotenv()


class MLService:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.model = model_name
        self.encoding = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def base64_image(self, image_path: str) -> str:
        """Helper to convert image file to base64 string."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def call_llm(
        self,
        messages: list,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        response_format: str = "text",
        call_type: str = "llm_call",
        max_retries: int = 3,
    ):
        model = model or self.model
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format != "text":
            payload["response_format"] = {"type": response_format}

        backoff = 2.0
        for attempt in range(1, max_retries + 2):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                usage = result.get("usage", {})

                return content, {
                    "type": call_type,
                    "model": model,
                    "usage": usage,
                    "cost": self.calculate_text_model_cost(usage, model)
                }

            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                body = e.response.text or ""
                retry_after = e.response.headers.get("Retry-After")
                retriable = (status == 429) or (status in (500, 502, 503, 504))

                if retriable and attempt <= max_retries:
                    if status == 429:
                        if retry_after:
                            wait_sec = float(retry_after) + 1.0
                        else:
                            import re
                            m = re.search(r"try again in ([\d.]+) seconds", body)
                            wait_sec = (float(m.group(1)) + 1.0) if m else backoff
                    else:
                        wait_sec = backoff

                    print(f"[{call_type}] HTTP {status}. Retrying in {wait_sec:.2f}s... [Attempt {attempt}/{max_retries}]")
                    time.sleep(wait_sec)
                    backoff = min(backoff * 2, 30.0)
                    continue

                # Non-retriable or exhausted
                print(f"[{call_type}] HTTPError {status}: {body[:500]}")
                raise

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt <= max_retries:
                    print(f"[{call_type}] Network error: {e}. Retrying in {backoff:.2f}s... [Attempt {attempt}/{max_retries}]")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 30.0)
                    continue
                print(f"[{call_type}] Network error, no more retries: {e}")
                raise

            except Exception as e:
                print(f"[{call_type}] Unexpected error: {e}")
                raise

    def calculate_text_model_cost(self, usage: dict, model_name: str) -> float:
        pricing = {
            "gpt-4o-mini": {"prompt": 0.15, "prompt_cached": 0.075, "completion": 0.60},
            "gpt-4o": {"prompt": 2.50, "prompt_cached": 1.25, "completion": 10.00},
            "gpt-4.1-mini": {"prompt": 0.40, "prompt_cached": 0.10, "completion": 1.60},
        }

        if model_name not in pricing:
            return 0.0

        prompt_tokens = usage.get("prompt_tokens", 0)
        cached_tokens = usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
        live_prompt = prompt_tokens - cached_tokens
        completion_tokens = usage.get("completion_tokens", 0)

        p = pricing[model_name]
        cost = (
            (live_prompt * p["prompt"]) +
            (cached_tokens * p["prompt_cached"]) +
            (completion_tokens * p["completion"])
        ) / 1_000_000
        return round(cost, 6)
