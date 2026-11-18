# effects.py — библиотека эффектов, совместимых с uperlin_viper.
#
# Все эффекты имеют единую сигнатуру:
#   fill_xxx(buf, pal, n, xs, t, o)
# где:
#   buf — bytearray буфера neopixel (strip.buf)
#   pal — палитра (bytes, 256×3)
#   n   — число LED
#   xs  — масштаб вдоль ленты (X_SCALE)
#   t   — координата времени (frame counter)
#   o   — кортеж ORDER (порядок каналов: (1,0,2,3) = GRB)

from uperlin_viper import uperlin8
import random


# ============================================================
# Пламя и его вариации
# ============================================================

def fill_flame(buf, pal, n, xs, t, o):
    """Классическое пламя: позиция × время."""
    o0, o1, o2 = o
    for i in range(n):
        v = uperlin8(i * xs, t)
        idx = v * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


def fill_flame_octaves(buf, pal, n, xs, t, o):
    """Пламя с двумя октавами — больше деталей и «рваности»."""
    o0, o1, o2 = o
    for i in range(n):
        v1 = uperlin8(i * xs, t)
        v2 = uperlin8(i * xs * 2 + 1000, t * 2)
        v = (v1 * 2 + v2) // 3
        idx = v * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


def fill_flame_wind(buf, pal, n, xs, t, o):
    """Пламя качается на «ветру» — координата сдвигается медленным шумом."""
    o0, o1, o2 = o
    wind = uperlin8(0, t // 4)
    shift = (wind - 128) * xs * 8
    for i in range(n):
        v = uperlin8(i * xs + shift, t)
        idx = v * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


def fill_twinkle(buf, pal, n, xs, t, o):
    """Пламя + случайные искры."""
    fill_flame(buf, pal, n, xs, t, o)
    for _ in range(random.randint(2, 4)):
        i = random.randint(0, n - 1)
        pos = i * 3
        buf[pos + o[0]] = 255
        buf[pos + o[1]] = 255
        buf[pos + o[2]] = 200


# ============================================================
# Движение
# ============================================================

def fill_comet(buf, pal, n, xs, t, o):
    """Комета с шумовым хвостом."""
    o0, o1, o2 = o
    head = (t * 4) % (n * 2) - n // 2
    tail = 20
    for i in range(n):
        pos = i * 3
        dist = abs(i - head)
        if dist < tail:
            intensity = 255 - (dist * 255) // tail
            v = (intensity * uperlin8(i * 40, t)) // 255
            idx = v * 3
            buf[pos + o0] = pal[idx]
            buf[pos + o1] = pal[idx + 1]
            buf[pos + o2] = pal[idx + 2]
        else:
            buf[pos + o0] = 0
            buf[pos + o1] = 0
            buf[pos + o2] = 0


def fill_rainbow_flow(buf, pal, n, xs, t, o):
    """Радуга течёт по ленте. Использовать с палитрой RAINBOW!"""
    o0, o1, o2 = o
    for i in range(n):
        v = (i * 4 + t * 5) & 0xFF
        idx = v * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


# ============================================================
# Органические волны
# ============================================================

def fill_aurora(buf, pal, n, xs, t, o):
    """Северное сияние: две медленные волны накладываются."""
    o0, o1, o2 = o
    for i in range(n):
        a = uperlin8(i * xs // 3, t // 6)
        b = uperlin8(i * xs // 2, t // 4 + 500)
        v = (a + b) // 2
        idx = v * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


def fill_pulse(buf, pal, n, xs, t, o):
    """Вся лента дышит синхронно."""
    o0, o1, o2 = o
    v_base = uperlin8(0, t * 2)
    for i in range(n):
        v = uperlin8(i * xs * 2, t * 2)
        v_mix = (v_base * 4 + v) // 5
        idx = v_mix * 3
        pos = i * 3
        buf[pos + o0] = pal[idx]
        buf[pos + o1] = pal[idx + 1]
        buf[pos + o2] = pal[idx + 2]


# ============================================================
# Точечные эффекты
# ============================================================

def fill_lightning(buf, pal, n, xs, t, o):
    """Молнии: редкие яркие вспышки на тёмном фоне."""
    o0, o1, o2 = o
    for i in range(n):
        pos = i * 3
        buf[pos + o0] = 0
        buf[pos + o1] = 0
        buf[pos + o2] = 0
    if uperlin8(t * 7, t * 3) > 230:
        for _ in range(random.randint(1, 2)):
            start = random.randint(0, n - 1)
            length = random.randint(5, 25)
            for j in range(length):
                i = (start + j) % n
                v = uperlin8(i * 30, t)
                idx = v * 3
                pos = i * 3
                buf[pos + o0] = pal[idx]
                buf[pos + o1] = pal[idx + 1]
                buf[pos + o2] = pal[idx + 2]


def fill_fireflies(buf, pal, n, xs, t, o):
    """Светлячки: разбросанные точки с разными ритмами."""
    o0, o1, o2 = o
    for i in range(n):
        v = uperlin8(i * 127, t // 3)
        pos = i * 3
        if v > 190:
            bright = (v - 190) * 4
            if bright > 255:
                bright = 255
            idx = bright * 3
            buf[pos + o0] = pal[idx]
            buf[pos + o1] = pal[idx + 1]
            buf[pos + o2] = pal[idx + 2]
        else:
            buf[pos + o0] = 0
            buf[pos + o1] = 0
            buf[pos + o2] = 0