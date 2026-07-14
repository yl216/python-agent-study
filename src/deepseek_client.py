from openai import OpenAI

from settings import Settings


def ask_deepseek(
    messages: list[dict[str, str]],
    settings: Settings,
    system_prompt: str,
) -> str:
    client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)
    response = client.chat.completions.create(
        model=settings.model,
        messages=[{"role": "system", "content": system_prompt}, *messages],
        temperature=settings.temperature,
        stream=False,
    )
    return response.choices[0].message.content or ""
