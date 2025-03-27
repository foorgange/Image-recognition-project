
import sys
from pathlib import Path
import logging

from src.my_app.utils.args_parser import parse_args
from src.my_app.utils.logger import setup_logger
from src.my_app.utils.config_loader import load_config
from src.my_app.models.yolo_model import YOLOModel
from src.my_app.videos.video_processor import VideoProcessor

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置（命令行参数优先）
    if args.video:
        config['video_input'] = args.video
    if args.device:
        config['model']['device'] = args.device
    if args.show:
        config['processing']['display_window'] = True
    if args.save:
        config['processing']['save_video'] = True
    
    # 设置日志
    setup_logger("my_app", config)
    logger = logging.getLogger("my_app")
    
    try:
        # 初始化模型
        model = YOLOModel(config['model'])
        
        # 初始化视频处理器
        processor = VideoProcessor(config, model)
        
        # 处理视频
        processor.process_video()
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        sys.exit(1)
        
    logger.info("处理完成")

if __name__ == "__main__":
    main()