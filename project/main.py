import morse_code
import timer_module
import simon_says
import asyncio

win = 0

morse_code_game = morse_code.Morsecode(3, 4, 6)
timer = timer_module.Timer()
simon_says_game = simon_says.SimonSays(5, 5, 3, 9, 10, 11, 12, 13, 4)


async def loop():
    global morse_code_game, win, strikes, timer

    while timer.current_strikes <= 3:

        timer_task = asyncio.create_task(timer.strikes())
        morse_task = asyncio.create_task(morse_code_game.main())
        morsecode_result = await morse_task

        if morsecode_result == "code lose":
            await timer.add_strike()
        else:
            win += 1

        if strikes > 0:
            await timer.strikes()

        timer_task.cancel()
        try:
            await timer_task
        except asyncio.CancelledError:
            pass
        morse_task.cancel()

asyncio.run(loop())