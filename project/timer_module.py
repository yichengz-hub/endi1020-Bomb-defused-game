from engi1020.arduino.api import *
import asyncio

class Timer():
    def __init__(self, led_pins: tuple):
        self.strike_leds = led_pins
        self.current_strike = 0
        self._lock = asyncio.Lock()

    async def strikes(self):
        while True:
            async with self._lock:
                for pin in self.strike_leds:
                    digital_write(pin, True)
            await asyncio.sleep(0.1)

    async def add_strike(self):
        async with self._lock:
            self.current_strike += 1