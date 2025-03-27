import cv2
import time
import logging
from pathlib import Path
from ..reports.visualization import DetectionVisualizer
from ..reports.metrics import DetectionMetrics

class VideoProcessor:
    def __init__(self, config, detector):
        self.config = config
        self.detector = detector
        self.logger = logging.getLogger(__name__)
        
        # 初始化可视化工具
        class_names = self._load_class_names()
        self.visualizer = DetectionVisualizer(class_names)
        
        # 初始化指标收集器
        self.metrics = DetectionMetrics() if config['metrics']['enabled'] else None
        
    def _load_class_names(self):
        """加载类别名称"""
        try:
            class_names_file = self.config['model']['class_names_file']
            with open(class_names_file, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            self.logger.warning(f"无法加载类别名称文件: {e}")
            return None
            
    def process_video(self, video_path=None):
        """处理视频文件或摄像头流"""
        video_path = video_path or self.config['video_input']
        cap = cv2.VideoCapture(video_path if video_path != "0" else 0)
        
        if not cap.isOpened():
            self.logger.error(f"无法打开视频源: {video_path}")
            return
            
        # 设置输出视频写入器
        out = None
        if self.config['processing']['save_video']:
            out = self._setup_video_writer(cap)
            
        try:
            self._process_frames(cap, out)
        finally:
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
            
        # 保存指标报告
        if self.metrics and self.config['metrics']['save_report']:
            self._save_metrics_report()
            
    def _setup_video_writer(self, cap):
        """设置视频写入器"""
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        output_path = Path(self.config['output_dir']) / "output.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        return cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (width, height)
        )
        
    def _process_frames(self, cap, out):
        """处理视频帧"""
        frame_count = 0
        
        while True:
            start_time = time.time()
            ret, frame = cap.read()
            
            if not ret:
                break
                
            # 执行检测
            detections = self.detector.detect(frame)
            
            if detections is not None:
                # 绘制检测结果
                if self.config['visualization']['draw_boxes']:
                    frame = self.visualizer.draw_detections(frame, detections)
                
                # 保存检测帧
                if (self.config['processing']['save_frames'] and 
                    frame_count % self.config['processing']['frame_save_interval'] == 0):
                    self.visualizer.save_detection_image(
                        frame, detections, self.config['output_dir']
                    )
                
                # 更新指标
                if self.metrics:
                    processing_time = time.time() - start_time
                    self.metrics.update(detections, processing_time)
            
            # 显示FPS
            if self.config['processing']['show_fps']:
                fps = 1.0 / (time.time() - start_time)
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 保存视频
            if out:
                out.write(frame)
            
            # 显示画面
            if self.config['processing']['display_window']:
                cv2.imshow('Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            frame_count += 1
            
    def _save_metrics_report(self):
        """保存性能指标报告"""
        import json
        from datetime import datetime
        
        report = self.metrics.get_summary()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(self.config['output_dir']) / f"metrics_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
        self.logger.info(f"性能指标报告已保存至: {report_path}")