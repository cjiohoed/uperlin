# uperlin_viper.py — целочисленный шум Перлина для MicroPython ESP32
# Основано на GyverLibs/uPerlin (который, в свою очередь, базируется на FastLED)
# Все вычисления — целочисленные, в Viper-режиме.

import micropython

# Таблица перестановок (256 + 1 дубликат первого элемента для безопасного "x+1")
_PERM = bytes([
    151, 160, 137,  91,  90,  15, 131,  13, 201,  95,  96,  53, 194, 233,   7, 225,
    140,  36, 103,  30,  69, 142,   8,  99,  37, 240,  21,  10,  23, 190,   6, 148,
    247, 120, 234,  75,   0,  26, 197,  62,  94, 252, 219, 203, 117,  35,  11,  32,
     57, 177,  33,  88, 237, 149,  56,  87, 174,  20, 125, 136, 171, 168,  68, 175,
     74, 165,  71, 134, 139,  48,  27, 166,  77, 146, 158, 231,  83, 111, 229, 122,
     60, 211, 133, 230, 220, 105,  92,  41,  55,  46, 245,  40, 244, 102, 143,  54,
     65,  25,  63, 161,   1, 216,  80,  73, 209,  76, 132, 187, 208,  89,  18, 169,
    200, 196, 135, 130, 116, 188, 159,  86, 164, 100, 109, 198, 173, 186,   3,  64,
     52, 217, 226, 250, 124, 123,   5, 202,  38, 147, 118, 126, 255,  82,  85, 212,
    207, 206,  59, 227,  47,  16,  58,  17, 182, 189,  28,  42, 223, 183, 170, 213,
    119, 248, 152,   2,  44, 154, 163,  70, 221, 153, 101, 155, 167,  43, 172,   9,
    129,  22,  39, 253,  19,  98, 108, 110,  79, 113, 224, 232, 178, 185, 112, 104,
    218, 246,  97, 228, 251,  34, 242, 193, 238, 210, 144,  12, 191, 179, 162, 241,
     81,  51, 145, 235, 249,  14, 239, 107,  49, 192, 214,  31, 181, 199, 106, 157,
    184,  84, 204, 176, 115, 121,  50,  45, 127,   4, 150, 254, 138, 236, 205,  93,
    222, 114,  67,  29,  24,  72, 243, 141, 128, 195,  78,  66, 215,  61, 156, 180,
    151,
])

# ============================================================
# Вспомогательные Viper-функции (все — нативные)
# ============================================================

@micropython.viper
def _wrap8(v: int) -> int:
    """Приведение к знаковому 8-битному целому."""
    v = v & 0xFF
    if v >= 128:
        v = v - 256
    return v


@micropython.viper
def _ease8(v: int) -> int:
    """Квадратичная интерполяция (FastLED-совместимая)."""
    v = v & 0xFF
    if v & 0x80:
        m = 255 - v
    else:
        m = v
    s = (m * (m + 1)) >> 8
    jj = (s << 1) & 0xFF
    if v & 0x80:
        return 255 - jj
    return jj


@micropython.viper
def _lerp8(a: int, b: int, frac: int) -> int:
    """Линейная интерполяция по 8-битным значениям."""
    frac = frac & 0xFF
    if b > a:
        d = (b - a) & 0xFF
        r = a + ((d * (frac + 1)) >> 8)
    else:
        d = (a - b) & 0xFF
        r = a - ((d * (frac + 1)) >> 8)
    return _wrap8(r)


@micropython.viper
def _grad1_8(h: int, x: int) -> int:
    """Градиент для 1D-шума."""
    h = h & 0xFF
    if h & 8:
        if ((h ^ (h >> 1)) & 1):
            half = (x + 1) >> 1
            return -half if (h & 1) else half
        return _wrap8(-x) if (h & 1) else x
    gu = 1 if (h & 4) else x
    gv = x if (h & 4) else 1
    if h & 1:
        gu = _wrap8(-gu)
    if h & 2:
        gv = _wrap8(-gv)
    gh = gu >> 1
    ghh = gv >> 1
    return _wrap8(gh + ghh + (gu - (gh << 1)))


@micropython.viper
def _grad2_8(h: int, x: int, y: int) -> int:
    """Градиент для 2D-шума."""
    if h & 4:
        gu = y
        gv = x
    else:
        gu = x
        gv = y
    if h & 1:
        gu = _wrap8(-gu)
    if h & 2:
        gv = _wrap8(-gv)
    gh = gu >> 1
    ghh = gv >> 1
    return _wrap8(gh + ghh + (gu - (gh << 1)))


@micropython.viper
def _scale_output8(raw: int) -> int:
    """Масштабирование из [-128,127] в [0,255]."""
    s = raw + 64
    if s <= 0:
        return 0
    d = s << 1
    return 255 if d > 255 else d


# ============================================================
# Основные функции шума (Viper)
# ============================================================

@micropython.viper
def _uperlin8_1d(x: int, perm: ptr8) -> int:
    cx = (x >> 8) & 0xFF
    u = x & 0xFF
    xx = (u >> 1) & 0x7F
    xx1 = xx - 128

    # hash1(cx) = (perm[perm[cx]], perm[perm[cx+1]])
    ha = perm[perm[cx]]
    hb = perm[perm[(cx + 1) & 0xFF]]

    u_eased = _ease8(u)
    raw = _lerp8(_grad1_8(ha, xx), _grad1_8(hb, xx1), u_eased)
    return _scale_output8(raw)


@micropython.viper
def _uperlin8_2d(x: int, y: int, perm: ptr8) -> int:
    # hash2(cx, cy) — 4 угла
    cx = (x >> 8) & 0xFF
    cy = (y >> 8) & 0xFF
    pa = perm[cx]
    pb = perm[(cx + 1) & 0xFF]
    pa_y = (pa + cy) & 0xFF
    pb_y = (pb + cy) & 0xFF
    haa = perm[pa_y]
    hab = perm[(pa_y + 1) & 0xFF]
    hba = perm[pb_y]
    hbb = perm[(pb_y + 1) & 0xFF]

    # Дробные части и их mirror-координаты
    u = x & 0xFF
    v = y & 0xFF
    xx = (u >> 1) & 0x7F
    yy = (v >> 1) & 0x7F
    xx1 = xx - 128
    yy1 = yy - 128

    # Ease-интерполяция
    u_eased = _ease8(u)
    v_eased = _ease8(v)

    # Билинейная интерполяция градиентов
    a = _lerp8(_grad2_8(haa, xx, yy), _grad2_8(hba, xx1, yy), u_eased)
    b = _lerp8(_grad2_8(hab, xx, yy1), _grad2_8(hbb, xx1, yy1), u_eased)
    raw = _lerp8(a, b, v_eased)
    return _scale_output8(raw)


# ============================================================
# Публичный API (тонкие Python-обёртки)
# ============================================================

def uperlin8(x, y=None):
    """8-битный шум Перлина (0..255). 1D или 2D."""
    if y is None:
        return _uperlin8_1d(int(x) & 0xFFFFFFFF, _PERM)
    return _uperlin8_2d(int(x) & 0xFFFFFFFF, int(y) & 0xFFFFFFFF, _PERM)