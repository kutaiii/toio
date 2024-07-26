import asyncio

from toio import *

async def rotate(cube:ToioCoreCube):
    await cube.api.motor.motor_control(10,-10)
    


async def main():
    async with ToioCoreCube() as cube:
        await rotate(cube)
        await cube.api.motor.motor_control(0,0)

    return 0


if __name__ == "__main__":
    asyncio.run(main())