"""短期对话记忆 —— 滑动窗口 可选摘要"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from src.utils.config_loader import config

class WindowedMemory:
    """封装带窗口大小的聊天历史, 自动截断"""

    def __init__(self, k: int = 10):
        self.history = InMemoryChatMessageHistory()
        self.k = k * 2          # 保存 k 对问答

    def add_messages(self, messages):
        """添加消息并自动修剪窗口"""
        self.history.add_messages(messages)
        all_msgs = self.history.messages
        if len(all_msgs) > self.k:
            # 保留最近 self.k 条消息
            trimmed = all_msgs[-self.k:]
            # 重新构建历史
            self.history.clear()
            self.history.aadd_messages(trimmed)

    @property
    def messages(self):
        return self.history.messages
    
    def clear(self):
        self.history.clear

def get_short_term_memory() -> WindowedMemory:
    """创建窗口式短期记忆实例"""
    window_size = config.get("memory.short_term.window_size", 10)
    return WindowedMemory(k=window_size)