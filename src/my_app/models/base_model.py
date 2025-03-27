from abc import ABC, abstractmethod
import torch

class BaseModel(ABC):
    """所有检测模型的基类"""
    
    def __init__(self, config):
        self.config = config
        self.device = torch.device(config.get('device', 'cuda') 
                                 if torch.cuda.is_available() else 'cpu')
        self.model = None
    
    @abstractmethod
    def load_model(self):
        """加载模型的抽象方法"""
        pass
    
    @abstractmethod
    def predict(self, image):
        """模型预测的抽象方法"""
        pass
    
    def to_device(self):
        """将模型移动到指定设备"""
        if self.model is not None:
            self.model.to(self.device) 