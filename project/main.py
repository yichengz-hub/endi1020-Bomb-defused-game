import asyncio
import time
from engi1020.arduino.api import *

from timer_module import select_time, run_timer
from simon_says import SimonSays
from passwords import Passwords
from morse_code import MorseCode


# ---------------- PIN CONFIG ----------------
RELAY_1 = 4   # simon / next
RELAY_2 = 7   # passwords / next
RELAY_3 = 6   # morse / next grove kit

PARTNER_SIGNAL_OUT = 15
PARTNER_SIGNAL = 16


# ---------------- HELPERS ----------------
async def set_relay(pin, state):
    digital_write(pin, state)
    await asyncio.sleep(0.5)


async def wait_for_partner_result():
    """
    Wait for one pulse = WIN
    Wait for second pulse within 2 sec = LOSE
    """
    print("Waiting for partner board result...")

    while not digital_read(PARTNER_SIGNAL):
        await asyncio.sleep(0.05)

    print("Pulse 1 detected")
    await asyncio.sleep(0.3)

    start = time.time()

    while time.time() - start < 2:
        if digital_read(PARTNER_SIGNAL):
            print("Pulse 2 detected -> LOSE")
            return "LOSE"
        await asyncio.sleep(0.05)

    print("Single pulse -> WIN")
    return "WIN"


async def check_explosion(game_state):
    while True:
        if game_state["exploded"]:
            print("💥 BOMB EXPLODED")
            return "LOSE"
        await asyncio.sleep(0.05)


async def run_with_bomb_watch(task_coro, game_state):
    """
    Runs a task while simultaneously watching for timer explosion.
    Returns either module result or LOSE.
    """
    module_task = asyncio.create_task(task_coro)
    bomb_task = asyncio.create_task(check_explosion(game_state))

    done, pending = await asyncio.wait(
        [module_task, bomb_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()

    return list(done)[0].result()


# ---------------- MAIN GAME ----------------
async def main():
    game_state = {"exploded": False}

    print("Select time with potentiometer...")
    start_time = select_time()

    timer_task = asyncio.create_task(run_timer(start_time, game_state))

    try:
        # =====================================
        # SIMON SAYS
        # =====================================
        print("Running Simon Says")
        await set_relay(RELAY_1, False)

        simon = SimonSays(2, 8, 9, 10, 11, 12, 13, 14, 15)

        round_num = 0
        strikes = 0
        colour_sequence = []
        first_time = True

        while strikes < 3:
            if game_state["exploded"]:
                print("💥 BOOM")
                return

            simon.start(
                initial_round=round_num,
                initial_strikes=strikes,
                initial_colours=colour_sequence
            )

            if first_time:
                await simon.increase_round()
                first_time = False

            result = await run_with_bomb_watch(simon.play(), game_state)

            if result == "WIN":
                print("Simon solved")
                break

            elif result == "Lose" or result == "LOSE":
                print("Simon failed")
                return

            round_num, strikes, colour_sequence = result

        if strikes >= 3:
            print("BOOM - Too many Simon strikes")
            return

        # =====================================
        # PASSWORDS
        # =====================================
        print("Running Passwords")
        await set_relay(RELAY_1, True)
        await set_relay(RELAY_2, False)

        password_game = Passwords(8, 9, 10)

        password_result = await run_with_bomb_watch(
            asyncio.to_thread(password_game.game_loop),
            game_state
        )

        if password_result != "WIN":
            print("💥 BOOM - Passwords failed")
            return

        print("Passwords solved")

        # =====================================
        # MORSE CODE
        # =====================================
        print("Running Morse Code")
        await set_relay(RELAY_2, True)
        await set_relay(RELAY_3, False)

        morse_game = MorseCode(11, 12, 13)
        morse_game.start(0)

        morse_result = await run_with_bomb_watch(
            morse_game.main(),
            game_state
        )

        if morse_result != "WIN":
            print("💥 BOOM - Morse failed")
            return

        print("Morse solved")

        # =====================================
        # PARTNER BOARD
        # =====================================
        print("Starting partner board")
        await set_relay(RELAY_3, True)

        digital_write(PARTNER_SIGNAL_OUT, True)
        await asyncio.sleep(0.5)
        digital_write(PARTNER_SIGNAL_OUT, False)

        partner_result = await run_with_bomb_watch(
            wait_for_partner_result(),
            game_state
        )

        if partner_result == "LOSE":
            print("💥 BOOM - Partner failed")
            return

        print("🎉 CONGRATULATIONS - BOMB DEFUSED 🎉")

    finally:
        timer_task.cancel()
        try:
            await timer_task
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
