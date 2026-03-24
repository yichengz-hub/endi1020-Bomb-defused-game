from morse_code import *

async def test():
    oled_clear()
    strikes = 0
    morse_test = MorseCode(3,4,6)
    while strikes < 3:
        morse_test.start(strikes)
        morse_task = asyncio.create_task(morse_test.main())
        while True:
            if morse_task.done():
                result = await morse_task
                if result == 'WIN':
                    return result
                else:
                    strikes = result
                    break
            await asyncio.sleep(0.1)
    print('YOU LOSE')
    return


asyncio.run(test())
