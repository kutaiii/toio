from toio.simple import SimpleCube
import sys
from connection.atom import AtomConnection, AtomSerialConnection
from slalm import *
import time
import signal
import matplotlib.pyplot as plt

LOOP = True
ATOM_MAC = "64:b7:08:80:e1:3c"
PORT ='COM3'
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


def test(config=config):
    cube = SimpleCube()
    atom = AtomSerialConnection(PORT)
    slam = SLAM(atom, cube, config)
    fig,ax = plt.subplots()
    im = ax.imshow(slam.get_map(), cmap='gray', vmin=0, vmax=2)
    while LOOP:
        # print(slam.mesurement.get_distance())
        # print(slam.mesurement.get_cube_location())
        slam.update()
        print(slam.get_map())
        im.set_data(slam.get_map())
        plt.pause(0.01)
        time.sleep(0.01)






if __name__ == "__main__":
    sys.exit(test())
