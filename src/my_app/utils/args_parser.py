import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='视频目标检测程序')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                        help='配置文件路径')
    parser.add_argument('--video', type=str,
                        help='输入视频路径，将覆盖配置文件中的设置')
    parser.add_argument('--device', type=str, choices=['cuda', 'cpu'],
                        help='运行设备，将覆盖配置文件中的设置')
    parser.add_argument('--show', action='store_true',
                        help='显示检测窗口')
    parser.add_argument('--save', action='store_true',
                        help='保存检测结果视频')
    
    return parser.parse_args() 