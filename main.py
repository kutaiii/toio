from toio.simple import SimpleCube
from toio.cube import ToioCoreCube
import sys
from connection.atom import *
from connection.cube import *
from slalm import *
import time
import signal
import matplotlib.pyplot as plt
import threading
import asyncio
import nest_asyncio
nest_asyncio.apply()

#TODO　toioの移動とmappingを同時に行うため、全体を非同期処理に変更する　Change the entire process to asynchronous processing in order to move and map toio at the same time

LOOP = True
TOIO_NAME = "toio-H6r"
ATOM_MAC = "64:b7:08:80:e1:3c" #bluetooth接続に使用　環境にあわせて変更  change to suit your environment
ATOM_IP = "192.168.0.104" #WiFi接続に使用　環境にあわせて変更  change to suit your environment
PORT ='COM3' #Serial接続に使用　環境にあわせて変更  change to suit your environment
MAX_X = 326
MIN_X = 43
MAX_Y = 240
MIN_Y = 46
MAPCONFIG = MapSetting(MAX_X, MIN_X, MAX_Y, MIN_Y)

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False
signal.signal(signal.SIGINT, ctrl_c_handler)

async def connect():
    try:
        cube = await connect_toio(TOIO_NAME)
        atom = AtomSerialConnection(PORT) #WiFi接続の場合はAtomWiFiConnection(ATOM_IP)に変更
        slam = SLAM(atom, cube, MAPCONFIG)
        return slam
    except:
        print("No cubes found")
        sys.exit(1)


async def slam_main(slam: SLAM):
    slam = slam
    fig,ax = plt.subplots()
    #fig2,ax2 = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='jet', vmin=0, vmax=2)
    #im2 = ax2.imshow(slam.get_colored_map(), cmap='jet', vmin=0, vmax=2)
    print(slam.cube.name)
    while LOOP:
        pos, angle = await slam.mesurement.get_cube_location()
        print(await slam.mesurement.get_distance())
        print(pos, angle)
        await slam.update()
        im.set_data(slam.get_map())
        # #im2.set_data(slam.get_colored_map())
        plt.pause(0.01)
        # time.sleep(0.01)
        await asyncio.sleep(0.01)
    # plt.close()
    # atom.disconnect()
    # return 0

async def move_main(slam: SLAM):
    slam = slam
    while LOOP:
        await slam.move()
        await asyncio.sleep(1)
    return 0


async def main():
    slam = await connect()
    await asyncio.gather(slam_main(slam),move_main(slam))
    



def main_sim(config):
    cube = CubeSiM()
    atom = AtomSimulatorConnection()
    slam = SLAM(atom, cube, config)
    fig,ax = plt.subplots()
    # fig2,ax2 = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='jet', vmin=0, vmax=2)
    # im2 = ax2.imshow(slam.get_colored_map(), cmap='jet', vmin=0, vmax=2)
    print("start")
    def update():
        while LOOP:
            slam.update()
            im.set_data(slam.get_map())
            # im2.set_data(slam.get_colored_map())
            print("update")
            plt.pause(0.01)
            time.sleep(0.01)
    def move():
        while LOOP:
            slam.move()
            time.sleep(1)
    thread = threading.Thread(target=move)
    thread.start()
    update()
    plt.close()
    return 0


if __name__ == "__main__":
    asyncio.run(main())
    
    

