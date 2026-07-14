import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-pro"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_HISTORY_TURNS = 5


class ConfigError(ValueError):
    """Raised when required app configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model: str
    temperature: float
    max_history_turns: int


def _read_required(name: str, placeholder: str | None = None) -> str:
    value = os.getenv(name, "").strip()
    if not value or value == placeholder:
        raise ConfigError(f"请先在 .env 里设置 {name}。")
    return value


def _read_float(name: str, default: float, min_value: float, max_value: float) -> float:
    raw_value = os.getenv(name, str(default)).strip()
    try:
        value = float(raw_value)
    except ValueError as error:
        raise ConfigError(f"{name} 必须是数字，当前值是：{raw_value}") from error

    if not min_value <= value <= max_value:
        raise ConfigError(f"{name} 必须在 {min_value} 到 {max_value} 之间，当前值是：{value}")
    return value


def _read_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw_value = os.getenv(name, str(default)).strip()
    try:
        value = int(raw_value)
    except ValueError as error:
        raise ConfigError(f"{name} 必须是整数，当前值是：{raw_value}") from error

    if not min_value <= value <= max_value:
        raise ConfigError(f"{name} 必须在 {min_value} 到 {max_value} 之间，当前值是：{value}")
    return value


def _read_url(name: str, default: str) -> str:
    value = os.getenv(name, default).strip().rstrip("/")
    if not value.startswith(("http://", "https://")):
        raise ConfigError(f"{name} 必须以 http:// 或 https:// 开头，当前值是：{value}")
    return value


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        api_key=_read_required("DEEPSEEK_API_KEY", "your_deepseek_api_key_here"),
        base_url=_read_url("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
        model=os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        temperature=_read_float("DEEPSEEK_TEMPERATURE", DEFAULT_TEMPERATURE, 0.0, 2.0),
        max_history_turns=_read_int("MAX_HISTORY_TURNS", DEFAULT_MAX_HISTORY_TURNS, 1, 20),
    )
