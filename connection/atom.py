import asyncio
import serial
from abc import ABC, abstractmethod

SCALE = 54/45 #atomによる距離とtoioマップの距離の比率

class AtomConnection:
    '''
    Atomとの接続を行う抽象クラス
    '''
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def distance(self):
        '''
        Atomとの距離を取得する
        get distance from Atom
        '''
        pass

class AtomSerialConnection(AtomConnection):
    '''
    シリアル接続クラス
    '''
    def __init__(self, port):
        self.port = port
        self.connect()
        
    def connect(self):
        self.ser = serial.Serial(self.port, 115200)

    def disconnect(self):
        self.ser.close()

    def distance(self):
        distance = self.ser.readline().decode('utf-8').strip()
        distance = float(distance)
        return distance/SCALE


class AtomBleConnection(AtomConnection):
    '''
    BLE接続クラス
    現環境でbluetoothの接続ができないため、未実装
    '''
    def __init__(self, mac):
        self.mac = mac
        self.connect()
        
    def connect(self):
        pass

    def disconnect(self):
        pass

    def distance(self):
        pass
    
    