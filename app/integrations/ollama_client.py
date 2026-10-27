import logging

from langchain_ollama import ChatOllama

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_llm() -> ChatOllama:
    logger.info("Creating Ollama client for model %s", settings.OLLAMA_MODEL)
    return ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0,
    )
