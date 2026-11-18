import time
from machine import Pin
import neopixel
from uperlin_viper import uperlin8
from palette import FIRE

NUM_LEDS  = 150
DATA_PIN  = 5
X_SCALE   = 60
TIME_STEP = 1
FRAME_MS  = 33

strip = neopixel.NeoPixel(Pin(DATA_PIN), NUM_LEDS)

# Локальные ссылки — ускоряют доступ в цикле
_pal = FIRE
_n   = NUM_LEDS
_xs  = X_SCALE
_noise = uperlin8

time_coord = 0

while True:
    for i in range(_n):
        v   = _noise(i * _xs, time_coord)
        idx = v * 3
        strip[i] = (_pal[idx], _pal[idx + 1], _pal[idx + 2])
    strip.write()
    time_coord += TIME_STEP
    time.sleep_ms(FRAME_MS)