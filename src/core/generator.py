from __future__ import annotations
import os
import json, re
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ Ollama not available. Using fallback LLM provider.")

load_dotenv()

DEFAULT_MODEL = os.getenv("LLM_MODEL", "mistral:7b-instruct")

def _strip_code_fences(txt: str) -> str:
    t = (txt or "").strip()
    t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()

def _extract_json_object(txt: str) -> Optional[str]:
    """
    Find the largest {...} block via brace counting. Helps when the model adds
    extra prose around the JSON or truncates trailing whitespace.
    """
    s = _strip_code_fences(txt)
    start = s.find("{")
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start:i+1]
    return None  # unmatched -> probably truncated

def try_fix_json(text: str) -> dict:
    s = _strip_code_fences(text)

    # 1) direct parse
    try:
        return json.loads(s)
    except Exception:
        pass

    # 2) extract the biggest {...} block and parse
    block = _extract_json_object(s)
    if block:
        try:
            return json.loads(block)
        except Exception:
            pass

    # 3) as a last resort, try to find a top-level array and wrap
    lst_s = s.find("[")
    lst_e = s.rfind("]")
    if lst_s != -1 and lst_e != -1 and lst_e > lst_s:
        arr = s[lst_s:lst_e+1]
        try:
            return {"items": json.loads(arr)}
        except Exception:
            pass

    # give up
    raise json.JSONDecodeError("Unable to recover valid JSON", s, 0)

class LLM(BaseModel):
    provider: str = "ollama"
    model: str = DEFAULT_MODEL

    def complete(self, prompt: str, temperature: float = 0.4, max_tokens: int = 800) -> str:
        if not OLLAMA_AVAILABLE:
            # Fallback response when ollama is not available
            return f"I'm sorry, but the AI model service is currently unavailable in this environment. Please try using the local version of SmartLearn or contact support for assistance.\n\nYour question was: {prompt}"
        
        system_msg = "You are a helpful educational assistant. Keep answers clear and age-appropriate."
        full = f"{system_msg}\n\nUser: {prompt}\nAssistant:"
        resp = ollama.generate(
            model=self.model,
            prompt=full,
            options={
                "temperature": float(temperature),
                "num_predict": int(max_tokens),
                "stop": ["\nUser:"],
            },
        )
        return resp.get("response", "").strip()

    def complete_json(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1800, attempts: int = 3) -> dict:
        """
        Use Ollama JSON mode. If the model returns invalid JSON, try to repair/extract.
        Retries a couple of times with slightly different nudges.
        """
        if not OLLAMA_AVAILABLE:
            # Fallback response when ollama is not available
            return {
                "error": "AI model service unavailable",
                "message": "The AI model service is currently unavailable in this environment. Please try using the local version of SmartLearn.",
                "fallback_data": {"items": []}
            }
        
        system_msg = "You are a helpful educational assistant. Only return valid JSON for structured tasks."
        for k in range(attempts):
            full = f"{system_msg}\n\nUser: {prompt}\nAssistant:"
            resp = ollama.generate(
                model=self.model,
                prompt=full,
                options={
                    "format": "json",          # ask for JSON
                    "temperature": float(temperature),
                    "num_predict": int(max_tokens),  # allow enough room for 8 Qs
                    "top_p": 0.9,
                    "stop": ["\nUser:"],
                },
            )
            txt = resp.get("response", "").strip()
            try:
                return try_fix_json(txt)
            except Exception:
                # light nudge: shorten explanations next attempt
                prompt = prompt + "\nMake explanations even shorter (<= 8 words). Return ONLY JSON."
                continue
        # if all attempts failed, raise the last error
        return try_fix_json(txt)
