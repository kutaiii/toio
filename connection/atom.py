import asyncio
import serial
from bleak import BleakClient
from abc import ABC, abstractmethod
import socket

SCALE = 54/45 #atomによる距離とtoioマップの距離の比率
TOIO_SIZE = 31.8 #toioの一辺の長さ

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

class AtomSimulatorConnection(AtomConnection):
    '''
    シミュレータ接続クラス
    '''
    def __init__(self):
        print("atom connect to simulator")

    def connect(self):
        pass

    def disconnect(self):
        pass

    def distance(self):
        return 0

class AtomSerialConnection(AtomConnection):
    '''
    シリアル接続クラス
    '''
    def __init__(self, port):
        self.port = port
        self.connect()
        print("atom connect to serial")
        
    def connect(self):
        self.ser = serial.Serial(self.port, 115200)

    def disconnect(self):
        self.ser.close()

    def distance(self):
        distance = self.ser.readline().decode('utf-8').strip()
        try:
            distance = float(distance)
            distance = distance - TOIO_SIZE/2
            return distance/SCALE
        except:
            return None


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

class AtomWiFiConnection(AtomConnection):
    '''
    WiFi接続クラス
    '''
    def __init__(self, ip):
        self.ip = ip
        self.port =5000
        self.buffer_size = 1024
        self.connect()
        print("atom connect to wifi")
        
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))

    def disconnect(self):
        self.client.close()

    def distance(self):
        distance = self.client.recv(self.buffer_size).decode('utf-8').strip()
        try:
            distance = float(distance)
            distance = distance-TOIO_SIZE/2
            return distance/SCALE
        except:
            return None

    