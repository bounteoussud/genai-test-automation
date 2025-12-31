# llm/ollama_client.py
import time
import requests
from utils.logger import get_logger

logger = get_logger("OllamaClient")

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt, model="llama3", retries=3):
    for attempt in range(retries):
        try:
            logger.info(f"Ollama call attempt {attempt + 1}")

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_ctx": 1024
                    }
                },
                timeout=300
            )

            data = response.json()
            logger.info(f"Ollama raw response keys: {list(data.keys())}")

            if "response" in data:
                return data["response"]

            if "error" in data:
                logger.error(f"Ollama error: {data['error']}")
                time.sleep(5)
                continue

            raise Exception(f"Unexpected Ollama response: {data}")

        except requests.exceptions.ReadTimeout:
            logger.warning("Ollama timeout, retrying...")
            time.sleep(5)

    raise Exception("Ollama failed after retries")
