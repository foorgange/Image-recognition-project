import numpy as np
from collections import defaultdict

class DetectionMetrics:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """重置所有指标"""
        self.total_frames = 0
        self.total_detections = 0
        self.processing_times = []
        self.class_counts = defaultdict(int)
        
    def update(self, detections, processing_time):
        """更新检测指标"""
        self.total_frames += 1
        self.total_detections += len(detections)
        self.processing_times.append(processing_time)
        
        for det in detections:
            cls_id = int(det[5])
            self.class_counts[cls_id] += 1
            
    def get_summary(self):
        """获取指标总结"""
        avg_fps = 1.0 / np.mean(self.processing_times) if self.processing_times else 0
        return {
            "total_frames": self.total_frames,
            "total_detections": self.total_detections,
            "average_fps": avg_fps,
            "average_detections_per_frame": self.total_detections / self.total_frames if self.total_frames > 0 else 0,
            "class_distribution": dict(self.class_counts)
        } 