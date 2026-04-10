"""Student-visible API for Arduino programming in labs.

This module re-exports selected functions and values from other modules to hide
some of the overall module's complexity. It can be imported with:

from engi1020.arduino.api import *

"""

from .io import analog_read, analog_write, digital_read, digital_write, buzzer_frequency, buzzer_note, buzzer_stop, tm1637_write
from .oled import clear as oled_clear, print_message as oled_print, move_cursor as oled_move_cursor
from .rgb_lcd import (
        clear as rgb_lcd_clear,
        set_colour as rgb_lcd_colour,
        print as rgb_lcd_print,

)

from .dht20 import (
        getTemp as temp_humid_get_temp,
        getHumidity as temp_humid_get_humidity
)

from .three_axis_accel import (
        getAccelX as three_axis_get_accelX,
        getAccelY as three_axis_get_accelY,
        getAccelZ as three_axis_get_accelZ,
)

from .pressure import (
        getTemperature as pressure_get_temp,
        getPressure as pressure_get_pressure,
        getAltitude as pressure_get_altitude,
)

from .servo import (
        setAngle as servo_set_angle,
        getAngle as servo_get_angle,
)

from .ultra_distance import (
        getCentimeters as ultra_get_centimeters,
        getInches as ultra_get_inches,
)

from .joystick import (
        getX as joystick_get_x,
        getY as joystick_get_y,
        getR_Theta as joystick_get_r_theta,
)

from .rgb_led import (
        set_colour_rgb as rgb_leds_colour_rgb,
        set_colour_hsv as rgb_leds_colour_hsv,
)

from .heart_rate import (
        start_monitor as heart_rate_start_monitor,
        get_rate as heart_rate_get_rate,
)