import logging
import os
from datetime import datetime


def setup_logger(name=__name__, config=None):
    if config is None:
        log_level = logging.INFO
        save_to_file = False
        log_file = None
    else:
        log_level = getattr(logging, config['logging']['level'].upper())
        save_to_file = config['logging']['save_to_file']
        log_file = config['logging']['log_file']

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出
    if save_to_file and log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger