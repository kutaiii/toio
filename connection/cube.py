from toio.cube import ToioCoreCube

class CubeSiM():
    def __init__(self):
        print("CubeSiM")

    def get_current_position(self):
        return 0, 0
    
    def get_orientation(self):
        return 0
    
    def turn(self, direction, angle):
        pass

    def move_to(self, speed, x, y):
        pass

    def move(self, speed, distance):
        pass

async def connect_toio(name):
    try:
        cube = ToioCoreCube(name=name)
        await cube.scan()
        await cube.connect()
        print("Connected")
        return cube
    except:
        print("No cubes found")



