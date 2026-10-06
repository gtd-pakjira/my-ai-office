import time

import requests


OLLAMA_URL = "http://host.docker.internal:11434"


def chat(
    message: str,
    system_prompt: str | None = None,
    response_format: str | None = None,
) -> str:
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt,
        })

    messages.append({
        "role": "user",
        "content": message,
    })

    payload = {
        # "model": "qwen3:4b",
        "model": "gemma3:4b",
        "messages": messages,
        "stream": False,
    }

    if response_format:
        payload["format"] = response_format

    print("[OLLAMA] Sending request...", flush=True)

    start_time = time.perf_counter()

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=False,
    )

    response.raise_for_status()

    elapsed = time.perf_counter() - start_time

    print(
        f"[OLLAMA] Response received in {elapsed:.2f}s",
        flush=True,
    )

    data = response.json()

    return data["message"]["content"]