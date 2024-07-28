from toio.simple import SimpleCube
import sys
from connection.atom import AtomConnection, AtomSerialConnection
from slalm import *
import time
import signal
import matplotlib.pyplot as plt

#TODO　toioの移動とmappingを同時に行うため、全体を非同期処理に変更する　Change the entire process to asynchronous processing in order to move and map toio at the same time

LOOP = True
ATOM_MAC = "64:b7:08:80:e1:3c" #bluetooth接続に使用　環境にあわせて変更  change to suit your environment
ATOM_IP = "192.168.0.104" #WiFi接続に使用　環境にあわせて変更  change to suit your environment
PORT ='COM3' #Serial接続に使用　環境にあわせて変更  change to suit your environment
MAX_X = 78
MIN_X = -205
MAX_Y = 205
MIN_Y = -13
MAPCONFIG = MapSetting(MAX_X, MIN_X, MAX_Y, MIN_Y)

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False
signal.signal(signal.SIGINT, ctrl_c_handler)


def main():
    cube = SimpleCube()
    atom = AtomSerialConnection(PORT) #WiFi接続の場合はAtomWiFiConnection(ATOM_IP)に変更
    slam = SLAM(atom, cube, MAPCONFIG)
    fig,ax = plt.subplots()
    fig2,ax2 = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='jet', vmin=0, vmax=2)
    im2 = ax2.imshow(slam.get_colored_map(), cmap='jet', vmin=0, vmax=2)
    while LOOP:
        slam.update()
        im.set_data(slam.get_map())
        im2.set_data(slam.get_colored_map())
        plt.pause(0.01)
        time.sleep(0.01)
    plt.close()
    atom.disconnect()
    return 0





if __name__ == "__main__":
    sys.exit(main())
