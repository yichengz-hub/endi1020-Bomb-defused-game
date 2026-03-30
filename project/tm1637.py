# tm1637.py - ENGI 1020 Compatible Version
import time
from engi1020.arduino.api import digital_write

class TM1637:
    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        # In engi1020, digital_write handles the setup automatically
        digital_write(self.clk, 0)
        digital_write(self.dio, 0)

    def _start(self):
        digital_write(self.dio, 0)
        digital_write(self.clk, 0)

    def _stop(self):
        digital_write(self.dio, 0)
        digital_write(self.clk, 1)
        digital_write(self.dio, 1)

    def _write_byte(self, byte):
        for i in range(8):
            digital_write(self.clk, 0)
            digital_write(self.dio, (byte >> i) & 1)
            digital_write(self.clk, 1)
        digital_write(self.clk, 0)
        digital_write(self.dio, 1)
        digital_write(self.clk, 1)

    def show_seconds(self, t):
        """Displays a number up to 9999"""
        mapping = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]
        s = str(t).zfill(4)
        self._start()
        self._write_byte(0x40) # Command to write data
        self._stop()
        self._start()
        self._write_byte(0xc0) # Address of first digit
        for char in s:
            self._write_byte(mapping[int(char)])
        self._stop()