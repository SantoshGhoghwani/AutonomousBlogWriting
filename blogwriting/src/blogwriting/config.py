"""LLM configuration (local Ollama)."""
import os

from crewai import LLM
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature: float = 0.4) -> LLM:
    return LLM(
        model=f"ollama/{os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=temperature,
    )