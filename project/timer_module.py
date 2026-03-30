from engi1020.arduino.api import *
import asyncio
import tm1637
import time

# Initialize using the pins for Port D2
display = tm1637.TM1637(clk=3, dio=2)

def countdown(t):
    while t >= 0:
        # Simplest way: show the seconds remaining
        # We use .zfill(4) to make sure it fills all 4 digits (e.g. 0060)
        display.show(str(t).zfill(4))
        
        if t == 0:
            print("KABOOM!")
            # Add buzzer or LED code here
            
        time.sleep(1)
        t -= 1

countdown(10) # 10 second test




class Timer():
    def __init__(self, led_pins: tuple):
        self.strike_leds = led_pins
        self.current_strikes = 0
        self._lock = asyncio.Lock()

    async def strikes(self):
        while True:
            async with self._lock:
                for i in range(len(self.strike_leds)):
                    pin = self.strike_leds[i]
                    if i < self.current_strikes: 
                        digital_write(pin, True)
                    else:
                        digital_write(pin, False)
            await asyncio.sleep(0.1)

    async def add_strike(self):
        async with self._lock:
            self.current_strikes += 1
