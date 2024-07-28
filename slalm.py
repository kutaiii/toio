import numpy as np
from dataclasses import dataclass

@dataclass
class MappingConfig():
    max_x: float
    min_x: float
    max_y: float
    min_y: float


class Mapping():
    '''
    マッピングを行うクラス
    マップの値の意味
    0: 未探索
    1: 探索済み
    2: 障害物

    '''
    def __init__(self, config: MappingConfig):
        self.config = config
        self.map = self.create_map()

    def map_size(self):
        return (self.config.max_x - self.config.min_x, self.config.max_y - self.config.min_y)
    
    def create_map(self):
        size = self.map_size()
        return np.zeros(size)
    
    def update_map(self, x, y, value):
        self.map[x, y] = value

    def get_map(self):
        return self.map
    
    def get_map_value(self, x, y):
        return self.map[x, y]
    
    
        

