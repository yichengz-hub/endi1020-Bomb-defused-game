from engi1020.arduino.api import *
import asyncio
from time import time


class Timer:
    def __init__(self, pot_pin, clock_pin, dio_pin, buzzer_pin=5):
        """
        For the buzzer pin use the default one on the grove kit, thus pin 5.
        And for the pot pin you must use an analog pin, which has numbers 0-5 on the grove kit
        The analog pins can also act as digital, mapping to analog 0-5 to digital 14-19
        BUT this class expects the ANALOG number NOT THE DIGITAL SO USE 0-5!!!
        """
        self.buzzer_pin = buzzer_pin #5
        self.pot_pin = pot_pin  # this 3 is analog: D13 is the same pin
        self.clock_pin = clock_pin #3
        self.dio_pin = dio_pin #2

        self.max_time = 600 # Time is in seconds thus 600 = 10 minuites
        self.stable_threshold = 20
        self.stable_time = 3


    def pot_to_time(self, value):
        """
        Convert potentiometer (0–1023) to time in seconds
        """
        raw = int((value / 1023) * self.max_time)
        return round(raw / 5) * 5


    def display_time(self, seconds):
        """
        Show time on 7-segmented display
        """
        minutes = seconds // 60
        secs = seconds % 60
        display_value = minutes * 100 + secs

        tm1637_write(self.clock_pin, self.dio_pin, display_value)


    async def select_time(self):
        """
        User turns potentiometer to select time.
        When it stops moving, returns selected time in seconds.
        """

        last_value = analog_read(self.pot_pin)
        last_change_time = time()

        while True:
            value = analog_read(self.pot_pin)

            seconds = self.pot_to_time(value)

            self.display_time(seconds)

            if abs(value - last_value) > self.stable_threshold:
                last_change_time = time()
                last_value = value

            if time() - last_change_time > self.stable_time:
                print(f"Selected time: {seconds} seconds")
                return seconds

            await asyncio.sleep(0.1)


    async def run_timer(self, start_time, game_state):
        time_left = start_time

        while time_left >= 0 and not game_state["game_over"]:
            self.display_time(time_left)
            buzzer_note(self.buzzer_pin, 1200, 0.12)

            if time_left == 0:
                print("[TIMER] BOOM - time ran out")
                game_state["game_over"] = True
                game_state["exploded"] = True
                return "LOSE"

            await asyncio.sleep(1)
            time_left -= 1

        
if __name__ == "__main__":
    digital_write(4,False)
    async def test():
        print("Turn the potentiometer to choose a time...")

        timer = Timer(3,3,2,5)
        
        start_time =  await timer.select_time()
        game_state = {"game_over": False, "exploded": False}

        print(f"Starting countdown from {start_time} seconds")

        timer_task = asyncio.create_task(timer.run_timer(start_time, game_state))

        await timer_task

    asyncio.run(test())
    