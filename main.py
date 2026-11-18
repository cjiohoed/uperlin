import time
from machine import Pin
import neopixel
from uperlin_viper import uperlin8

NUM_LEDS = 150
strip = neopixel.NeoPixel(Pin(5), NUM_LEDS)

# Параметры пламени
X_SCALE = 60  # ширина "языков": больше = уже языки
TIME_STEP = 1  # скорость "дыхания" (1-3 для плавности)
FRAME_MS = 33  # 30 fps

time_coord = 0

while True:
	for i in range(NUM_LEDS):
		# 2D-шум: позиция вдоль ленты × время
		v = uperlin8(i * X_SCALE, time_coord)

		# Палитра: чёрный → тёмно-красный → оранжевый → жёлтый → белый
		if v < 32:
			r, g, b = v * 4, 0, 0
		elif v < 96:
			r, g, b = 128 + (v - 32) * 2, (v - 32) * 3, 0
		elif v < 160:
			r, g, b = 255, 192 + (v - 96), (v - 96) * 3
		else:
			r = g = b = 255

		strip[i] = (r, g, b)

	strip.write()
	time_coord += TIME_STEP
	time.sleep_ms(FRAME_MS)