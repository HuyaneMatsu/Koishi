__all__ = ()

from re import compile as re_compile

CUSTOM_ID_ROLL_PATTERN = re_compile('roll\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)')
CUSTOM_ID_ROLL_BUILDER = (
    lambda dice_count, dice_sides, fix_amount, luck :
    f'roll.{dice_count:x}.{dice_sides:x}.{(fix_amount >= 0):x}.{abs(fix_amount):x}.{(luck >= 0):x}.{abs(luck):x}'
)
