import os
import re 
import yaml
from dotenv import load_dotenv

class ConfigLoader: 
    """
    加载 config/settings.yaml, 解析占位符
    """
    def __init__(self, config_path: str = "config/settings.yaml"):
        # 加载 .env 配置
        load_dotenv("config/.env")
        with open(config_path, "r", encoding="utf-8") as f:
            raw = f.read()
        resolved = self._resolve_env(raw)
        self.config = yaml.safe_load(resolved)

    def _resolve_env(self, text: str) -> str:
        pattern = re.compile(r'\$\{([^}:]+)(?::([^}]*))?\}')

        def replacer(match):
            var = match.group(1)
            default = match.group(2)
            return os.getenv(var, default)
        
        return pattern.sub(replacer, text)
    
    def get(self, key: str, default=None):
        """支持点号路径获取"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if  value is None:
                return default
        return value

# 其他模块直接导入使用    
config = ConfigLoader()