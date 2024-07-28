import numpy as np
from dataclasses import dataclass
from connection.atom import AtomConnection
from toio.simple import SimpleCube

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

    map value
    0: not searched
    1: searched
    2: obstacle
    '''
    def __init__(self, config: MappingConfig):
        self.config = config
        self.map = self.create_map()

    def map_size(self):
        return (self.config.max_x - self.config.min_x, self.config.max_y - self.config.min_y)
    
    def create_map(self):
        size = self.map_size()
        return np.zeros(size)
    
    def locatin_correction(self, x, y, orientation):
        '''
        位置情報をマップの座標に変換する
        '''
        x = int(x)
        y = int(y)
        x = x - self.config.min_x
        y = y - self.config.min_y
        orientation = orientation+90
        orientation = np.deg2rad(orientation)

        return x, y, orientation
    
    def update_map(self,x,y,angle,distance):
        '''
        マップを更新する
        '''
        x, y , angle = self.locatin_correction(x, y, angle)
        obstacle_x = x + distance * np.cos(angle)
        obstacle_y = y + distance * np.sin(angle)
        obstacle_x = int(obstacle_x)
        obstacle_y = int(obstacle_y)
        if self.map.shape[0] > obstacle_x >= 0 and self.map.shape[1] > obstacle_y >= 0:
            self.map[obstacle_x, obstacle_y] = 2
            

    def get_map(self):
        return self.map
    
    def get_map_value(self, x, y):
        return self.map[x, y]

class Mesurement():
    def __init__(self, atom: AtomConnection, cube: SimpleCube):
        self.atom = atom
        self.cube = cube

    def get_distance(self):
        '''
        Atomとの距離を取得する
        '''
        return self.atom.distance()
    
    def get_cube_location(self):
        '''
        Cubeの位置情報を取得する
        '''
        pos = self.cube.get_current_position()
        orientation = self.cube.get_orientation()
        return pos, orientation

class SLAM():
    def __init__(self, atom: AtomConnection, cube: SimpleCube, config: MappingConfig):
        self.atom = atom
        self.cube = cube
        self.mapping = Mapping(config)
        self.mesurement = Mesurement(atom, cube)
    
    def update(self):
        distance = self.mesurement.get_distance()
        pos, orientation = self.mesurement.get_cube_location()
        if distance is not None and pos is not None and orientation is not None:
            self.mapping.update_map(pos[0], pos[1], orientation, distance)
        return self.mapping.get_map()
    
    def get_map(self):
        return self.mapping.get_map()
    
    
        

