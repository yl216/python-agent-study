import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    api_key: str
    base_url: str
    model: str
    temperature: float
    max_history_turns: int


def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key or api_key == "your_deepseek_api_key_here":
        raise ValueError("请先在 .env 里设置 DEEPSEEK_API_KEY。")

    return Settings(
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip(),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro").strip(),
        temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.3")),
        max_history_turns=int(os.getenv("MAX_HISTORY_TURNS", "5")),
    )
