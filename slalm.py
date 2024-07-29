import numpy as np
from dataclasses import dataclass
from connection.atom import AtomConnection
from toio.simple import SimpleCube
from toio.cube import ToioCoreCube
import matplotlib.pyplot as plt

@dataclass
class MapSetting():
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
    def __init__(self, config: MapSetting):
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
        orientation = -orientation
        orientation = orientation-90
        orientation = np.deg2rad(orientation)

        return x, y, orientation
    
    def bresenham(self, x0, y0, x1, y1):
        '''
        ブレゼンハムアルゴリズム
        2点間の直線を引く
        障害物とtoioの間のマスを探索済みのマスとして返す
        '''
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = np.sign(x1 - x0)
        sy = np.sign(y1 - y0)
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return np.array(points)
    
    #TODO バグがあるので修正する
    def color_map_based_on_counts(self,cell_size=10):
        """
        マップをマス目に分けて、各マスの中の0,1,2の個数に応じてマスの色を決定する。
        
        Parameters:
        - cell_size: マス目のサイズ
        
        Returns:
        - colored_map: 色分けされたマップ
        """
        map_data = self.get_map()
        rows, cols = map_data.shape
        colored_map = np.zeros((rows // cell_size, cols // cell_size))

        for i in range(0, rows-rows%cell_size, cell_size):
            for j in range(0, cols, cell_size):
                cell = map_data[i:i + cell_size, j:j + cell_size]
                unique, counts = np.unique(cell, return_counts=True)
                count_dict = dict(zip(unique, counts))
                count_0 = count_dict.get(0, 0)
                count_1 = count_dict.get(1, 0)
                count_2 = count_dict.get(2, 0)
                
                if count_0 >2:
                    color = 0
                elif count_1 > 5:
                    color = 1
                else:
                    color = 2
                
                colored_map[i // cell_size-1, j // cell_size-1] = color

        return colored_map

    def update_map(self,x,y,angle,distance):
        '''
        マップを更新する
        '''
        x, y , angle = self.locatin_correction(x, y, angle)
        obstacle_x = x + distance * np.cos(angle)
        obstacle_y = y + distance * np.sin(angle)
        obstacle_x = int(obstacle_x)
        obstacle_y = int(obstacle_y)
        free_points = self.bresenham(x, y, obstacle_x, obstacle_y)
        if self.map.shape[0] > obstacle_x >= 0 and self.map.shape[1] > obstacle_y >= 0 and self.map.shape[0] > x >= 0 and self.map.shape[1] > y >= 0:
            self.map[free_points[:, 0], free_points[:, 1]] = 1
            self.map[obstacle_x, obstacle_y] = 2           

    def get_map(self):
        return self.map
    
    def get_map_value(self, x, y):
        return self.map[x, y]

class Measuring():
    def __init__(self, atom: AtomConnection, cube: ToioCoreCube):
        self.atom = atom
        self.cube = cube

    async def get_distance(self):
        '''
        Atomとの距離を取得する
        '''
        return await self.atom.distance()
    
    async def get_cube_location(self):
        '''
        Cubeの位置情報を取得する
        '''
        data = await self.cube.api.id_information.read()
        if  hasattr(data, 'center') and hasattr(data.center, 'point') and hasattr(data.center, 'angle'):
            pos = (data.center.point.x, data.center.point.y)
            angle = data.center.angle
            return pos, angle
        return None, None

class Moving():
    def __init__(self, cube: ToioCoreCube, config: MapSetting):
        self.cube = cube
        self.config = config

    def correct_position(self,x ,y):
        '''
        位置補正
        '''
        x = x + self.config.min_x
        y = y + self.config.min_y
        if x < self.config.min_x:
            x = self.config.min_x
        if x > self.config.max_x:
            x = self.config.max_x
        if y < self.config.min_y:
            y = self.config.min_y
        if y > self.config.max_y:
            y = self.config.max_y
        return x, y
        
    def rotate(self):
        '''
        その場で一周
        '''
        print("rotate")
        self.cube.turn(1,360)
    def turn(self, angle):
        '''
        指定角度回転
        '''
        self.cube.turn(1,angle)

    def move_to(self, x, y):
        '''
        指定位置まで移動
        '''
        x, y = self.correct_position(x, y)
        self.cube.move_to(10,x, y)

    def move(self,travel_distanvce):
        '''
        指定距離移動
        '''
        self.cube.move(travel_distanvce,1)
        

class SLAM():
    def __init__(self, atom: AtomConnection, cube: ToioCoreCube, config: MapSetting):
        self.atom = atom
        self.cube = cube
        self.mapping = Mapping(config)
        self.mesurement = Measuring(atom, cube)
        self.moving = Moving(cube, config)
    
    async def update(self):
        '''
        マップを更新する
        '''
        distance = await self.mesurement.get_distance()
        pos, orientation = await self.mesurement.get_cube_location()
        if (distance is not None) and (pos is not None) and (orientation is not None):
            self.mapping.update_map(pos[0], pos[1], orientation, distance)
        return self.mapping.get_map()
    
    def get_map(self):
        return self.mapping.get_map()
    
    def get_colored_map(self):
        return self.mapping.color_map_based_on_counts()
    
    def move(self):
        print("moving")
        self.moving.rotate()
        if self.mesurement.get_distance() is not None:
            if self.mesurement.get_distance() > 10:
                self.moving.move(10)
            else:
                self.moving.turn(90)
            

        
    
    

    
    
        

