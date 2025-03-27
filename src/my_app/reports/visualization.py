import cv2
import numpy as np
from datetime import datetime

class DetectionVisualizer:
    def __init__(self, class_names=None):
        self.class_names = class_names
        self.colors = np.random.uniform(0, 255, size=(len(class_names) if class_names else 80, 3))
        
    def draw_detections(self, image, detections):
        """在图像上绘制检测结果"""
        img = image.copy()
        for det in detections:
            bbox = det[:4].astype(int)
            conf = det[4]
            cls_id = int(det[5])
            
            color = self.colors[cls_id]
            label = f"{self.class_names[cls_id] if self.class_names else cls_id} {conf:.2f}"
            
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            cv2.putText(img, label, (bbox[0], bbox[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return img
    
    def save_detection_image(self, image, detections, output_path):
        """保存带有检测结果的图像"""
        img_with_det = self.draw_detections(image, detections)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_path}/detection_{timestamp}.jpg"
        cv2.imwrite(filename, img_with_det)
        return filename 