__all__ = ()

from ..farewell_style import FarewellStyle
from ..farewell_style_item import FarewellStyleItem

from .constants import IMAGE_CREATOR


NAME = 'flandre'


ITEMS = (
    FarewellStyleItem(
        (lambda target: f'{target} escaped the basement!!'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261948894028369970/flandre-farewell-0000.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'Just broke {target}!!'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971119020179456/flandre-farewell-0001.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'Pache, did {target} really just vanish under the sun???'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971120119353394/flandre-farewell-0002.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'Where is {target} going?'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971121427714099/flandre-farewell-0003.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'{target} isn\'t hiding under my bed anymore.'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971122606575616/flandre-farewell-0004.png',
        IMAGE_CREATOR,
    ),
)


FAREWELL_STYLE = FarewellStyle(
    NAME,
    ITEMS,
)
