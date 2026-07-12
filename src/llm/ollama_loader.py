"""Ollama 模型加载器 —— 基于 LangChain 的 ChatOllama"""

from langchain_ollama import ChatOllama
from src.utils.config_loader import config

def get_llm() -> ChatOllama:
    """根据配置创建 ChatOllama 实例, 用于 Agent 对话"""
    return ChatOllama(
        base_url=config.get("llm.base_url"),
        model=config.get("llm.model"),
        temperature=config.get("llm.temperature", 0.8),
    )