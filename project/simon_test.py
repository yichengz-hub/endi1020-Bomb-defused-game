from simon_says import *
import asyncio

async def test():
    simon_test = SimonSays(5, 5, 1, 2, 3, 4, 6, 7, 8)
    simon_test.start()
    simon_task = asyncio.create_task(simon_test.play())
    await simon_task


asyncio.run(test())
