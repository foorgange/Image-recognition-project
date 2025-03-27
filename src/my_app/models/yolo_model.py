from .base_model import BaseModel
import torch
import os

class YOLOModel(BaseModel):
    """YOLO模型实现类"""
    
    def __init__(self, config):
        super().__init__(config)
        self.confidence_threshold = config['confidence_threshold']
        self.iou_threshold = config['iou_threshold']
        self.model = self.load_model()
        self.class_names = self._load_class_names()
        
    def load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                             path=self.config['weights'])
        model.conf = self.confidence_threshold
        model.iou = self.iou_threshold
        self.to_device()
        return model
        
    def predict(self, image):
        results = self.model(image)
        return results.xyxy[0].cpu().numpy()

    def _load_class_names(self):
        """加载类别名称，使用UTF-8编码"""
        try:
            class_names_file = self.config.get('class_names_file')
            if class_names_file and os.path.exists(class_names_file):
                with open(class_names_file, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f.readlines()]
            return None
        except Exception as e:
            print(f"Error loading class names: {e}")
            return None 