import yaml
import os

def load_config(config_path="config/config.yaml"):
    """
    加载配置文件，使用UTF-8编码
    """
    try:
        with open(config_path, "r", encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None