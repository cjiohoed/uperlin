# palette.py — набор палитр в виде таблиц bytes (256×3 = R,G,B)
# Каждая палитра — готовый объект bytes, генерируется один раз при импорте.


def _build_fire_palette():
    """Классическое огненное пламя: чёрный → красный → оранжевый → белый."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = v * 4, 0, 0
        elif v < 96:
            t = v - 32
            r, g, b = 128 + t * 2, t * 3, 0
        elif v < 160:
            t = v - 96
            r, g, b = 255, 192 + t, t * 3
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_ice_palette():
    """Холодное синее газовое пламя."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = 0, 0, v * 4
        elif v < 96:
            t = v - 32
            r, g, b = 0, t * 3, 128 + t * 2
        elif v < 160:
            t = v - 96
            r, g, b = t * 3, 192 + t, 255
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_arcane_palette():
    """Зелёное магическое пламя."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = 0, v * 4, 0
        elif v < 96:
            t = v - 32
            r, g, b = 0, 128 + t * 2, 0
        elif v < 160:
            t = v - 96
            r, g, b = t * 2, 255, t * 2
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_plasma_palette():
    """Розово-фиолетовая энергия."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = v * 4, 0, v * 6
        elif v < 96:
            t = v - 32
            r, g, b = 128 + t * 2, t * 2, 192 + t
        elif v < 160:
            t = v - 96
            r, g, b = 255, 128 + t * 2, 255
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_toxic_palette():
    """Кислотно-зелёное радиоактивное свечение."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = v * 2, v * 6, 0
        elif v < 96:
            t = v - 32
            r, g, b = 64 + t, 192 + t, 0
        elif v < 160:
            t = v - 96
            r, g, b = 128 + t * 2, 255, t * 2
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_blood_palette():
    """Багровое адское пламя."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = v * 3, 0, 0
        elif v < 128:
            t = v - 64
            r, g, b = 192 + t, t, 0
        elif v < 200:
            t = v - 128
            r, g, b = 255, 64 + t * 2, 0
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_aurora_palette():
    """Северное сияние: зелёный → голубой → фиолетовый."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = 0, v * 4, v * 2
        elif v < 128:
            t = v - 64
            r, g, b = 0, 255, 128 + t * 2
        elif v < 192:
            t = v - 128
            r, g, b = t * 4, 255 - t * 2, 255
        else:
            t = v - 192
            r, g, b = 255, 64 - t // 2, 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_sunset_palette():
    """Закат: оранжевый → розовый → пурпур."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = v * 4, v, 0
        elif v < 128:
            t = v - 64
            r, g, b = 255, 64 + t * 2, t * 2
        elif v < 192:
            t = v - 128
            r, g, b = 255, 192 + t, 128 + t * 2
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_ocean_palette():
    """Глубина океана: тёмный синий → голубой → белый."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = 0, v // 2, v * 4
        elif v < 128:
            t = v - 64
            r, g, b = 0, 32 + t * 3, 255
        elif v < 192:
            t = v - 128
            r, g, b = t * 4, 224 + t, 255
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_gold_palette():
    """Золотой янтарь."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = v * 3, v, 0
        elif v < 128:
            t = v - 64
            r, g, b = 192 + t, 64 + t * 2, 0
        elif v < 200:
            t = v - 128
            r, g, b = 255, 192 + t, t * 2
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_ghost_palette():
    """Призрачное бело-голубое свечение."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 64:
            r, g, b = v, v * 2, v * 4
        elif v < 128:
            t = v - 64
            r, g, b = 64 + t, 128 + t * 2, 255
        elif v < 192:
            t = v - 128
            r, g, b = 192 + t, 255, 255
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_volcano_palette():
    """Вулкан: тёмная кора с раскалёнными трещинами."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 96:
            r, g, b = 0, 0, 0
        elif v < 160:
            t = v - 96
            r, g, b = t * 4, t, 0
        elif v < 220:
            t = v - 160
            r, g, b = 255, 64 + t * 3, 0
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_candle_palette():
    """Мягкое свечение свечи — низкая максимальная яркость."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 96:
            r, g, b = v * 2, v, 0
        elif v < 192:
            t = v - 96
            r, g, b = 192 + t // 2, 96 + t // 2, t // 3
        else:
            r, g, b = 230, 200, 128
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_neon_palette():
    """Электрический неон: фиолетовый → пурпурный → белый."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 32:
            r, g, b = v * 4, 0, v * 8
        elif v < 96:
            t = v - 32
            r, g, b = 128 + t * 2, 0, 255
        elif v < 160:
            t = v - 96
            r, g, b = 255, t * 2, 255 - t * 2
        else:
            r = g = b = 255
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


def _build_rainbow_palette():
    """Полный спектр радуги — для эффекта rainbow_flow."""
    pal = bytearray(256 * 3)
    for v in range(256):
        if v < 43:
            r, g, b = 255, v * 6, 0
        elif v < 85:
            t = v - 43
            r, g, b = 255 - t * 6, 255, 0
        elif v < 128:
            t = v - 85
            r, g, b = 0, 255, t * 6
        elif v < 170:
            t = v - 128
            r, g, b = 0, 255 - t * 6, 255
        elif v < 213:
            t = v - 170
            r, g, b = t * 6, 0, 255
        else:
            t = v - 213
            r, g, b = 255, 0, 255 - t * 6
        pal[v*3], pal[v*3+1], pal[v*3+2] = r, g, b
    return bytes(pal)


# ============================================================
# Собранные палитры — готовы к использованию после импорта
# ============================================================

FIRE    = _build_fire_palette()
ICE     = _build_ice_palette()
ARCANE  = _build_arcane_palette()
PLASMA  = _build_plasma_palette()
TOXIC   = _build_toxic_palette()
BLOOD   = _build_blood_palette()
AURORA  = _build_aurora_palette()
SUNSET  = _build_sunset_palette()
OCEAN   = _build_ocean_palette()
GOLD    = _build_gold_palette()
GHOST   = _build_ghost_palette()
VOLCANO = _build_volcano_palette()
CANDLE  = _build_candle_palette()
NEON    = _build_neon_palette()
RAINBOW = _build_rainbow_palette()