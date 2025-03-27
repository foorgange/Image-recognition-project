import torch
import logging

class Detector:
    def __init__(self, model_config):
        self.logger = logging.getLogger(__name__)
        self.config = model_config
        self.device = torch.device(model_config.get('device', 'cuda') if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_config)
        self.logger.info(f"模型已加载到设备: {self.device}")

    def _load_model(self, config):
        try:
            model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                 path=config['weights'])
            model.to(self.device)
            model.conf = config['confidence_threshold']
            model.iou = config['iou_threshold']
            return model
        except Exception as e:
            self.logger.error(f"模型加载失败: {str(e)}")
            raise

    def detect(self, frame):
        try:
            results = self.model(frame)
            return results.xyxy[0].cpu().numpy()  # 返回numpy数组格式的检测结果
        except Exception as e:
            self.logger.error(f"检测过程出错: {str(e)}")
            return None