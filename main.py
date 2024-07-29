from toio.simple import SimpleCube
import sys
from connection.atom import *
from connection.cube import *
from slalm import *
import time
import signal
import matplotlib.pyplot as plt
import threading

#非同期処理

LOOP = True
ATOM_MAC = "64:b7:08:80:e1:3c" #bluetooth接続に使用　環境にあわせて変更  change to suit your environment
ATOM_IP = "192.168.0.104" #WiFi接続に使用　環境にあわせて変更  change to suit your environment
PORT ='COM3' #Serial接続に使用　環境にあわせて変更  change to suit your environment
MAX_X = 78
MIN_X = -205
MAX_Y = 205
MIN_Y = -13
config = MappingConfig(MAX_X, MIN_X, MAX_Y, MIN_Y)

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False
signal.signal(signal.SIGINT, ctrl_c_handler)


def main(config):
    cube = SimpleCube()
    atom = AtomSerialConnection(PORT) #WiFi接続の場合はAtomWiFiConnection(ATOM_IP)に変更
    slam = SLAM(atom, cube, config)
    plt.ion()
    fig,ax = plt.subplots()
    fig2,ax2 = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='jet', vmin=0, vmax=2)
    im2 = ax2.imshow(slam.get_colored_map(), cmap='jet', vmin=0, vmax=2)
    def update():
        while LOOP:
            slam.update()
            im.set_data(slam.get_map())
            im2.set_data(slam.get_colored_map())
            time.sleep(0.01)
    thread = threading.Thread(target=update)
    thread.start()
    plt.close()
    atom.disconnect()
    return 0

def main_sim(config):
    cube = CubeSiM()
    atom = AtomSimulatorConnection()
    slam = SLAM(atom, cube, config)
    fig,ax = plt.subplots()
    fig2,ax2 = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='jet', vmin=0, vmax=2)
    im2 = ax2.imshow(slam.get_colored_map(), cmap='jet', vmin=0, vmax=2)
    print("start")
    def update():
        while LOOP:
            slam.update()
            im.set_data(slam.get_map())
            im2.set_data(slam.get_colored_map())
            plt.pause(0.01)
            time.sleep(0.01)
    def move():
        while LOOP:
            print("moving!")
            time.sleep(1)
    thread = threading.Thread(target=move)
    thread.start()
    update()
    plt.close()
    return 0





if __name__ == "__main__":
    sys.exit(main_sim(config))
