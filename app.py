import time
from machine import Pin
import neopixel

from config import *

strip = neopixel.NeoPixel(Pin(DATA_PIN), NUM_LEDS)
strip.brightness = BRIGHTNESS

try:
    buf = strip.buf
except AttributeError:
    raise RuntimeError("Требуется MicroPython 1.20+ с атрибутом neopixel.buf")

try:
    _ORDER = strip.ORDER
except AttributeError:
    _ORDER = (1, 0, 2, 3)


def benchmark():
    N = 10000
    t0 = time.ticks_us()
    for i in range(N):
        effects.uperlin8(i * 60, i)
    dt = time.ticks_diff(time.ticks_us(), t0)
    print("uperlin8: {:.1f} мкс/вызов".format(dt / N))

    t0 = time.ticks_us()
    EFFECT(buf, PAL, NUM_LEDS, X_SCALE, 0, _ORDER)
    dt_frame = time.ticks_diff(time.ticks_us(), t0)
    print("кадр: {} мкс (бюджет {} мкс)".format(
        dt_frame, FRAME_MS * 1000))


def main():
    t = 0
    frame_count = 0
    last_print = time.ticks_ms()

    while True:
        t_start = time.ticks_us()
        EFFECT(buf, PAL, NUM_LEDS, X_SCALE, t, _ORDER)
        strip.write()
        t_frame = time.ticks_diff(time.ticks_us(), t_start)

        t = (t + TIME_STEP) & 0xFFFFFFFF
        frame_count += 1

        if DEBUG_TIMING:
            now = time.ticks_ms()
            if time.ticks_diff(now, last_print) >= 2000:
                fps = frame_count * 1000.0 / time.ticks_diff(now, last_print)
                print("[timing] {:.1f} fps, кадр {} мкс".format(fps, t_frame))
                frame_count = 0
                last_print = now

        time.sleep_ms(FRAME_MS)