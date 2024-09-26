__all__ = ()

from ..farewell_style_item import FarewellStyleItem
from ..farewell_style import FarewellStyle

from .constants import IMAGE_CREATOR


NAME = 'koishi'


ITEMS = (
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261948895060037692/koishi-farewell-0000.png',
        IMAGE_CREATOR,
        (lambda target: f'What? {target} won\'t have dinner with us anymore??'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261963285260140594/koishi-farewell-0001.png',
        IMAGE_CREATOR,
        (lambda target: f'Oh, so {target} is gone? Who would have guessed...'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261963286526689301/koishi-farewell-0002.png',
        IMAGE_CREATOR,
        (lambda target: f'Satori, I just heard that {target} is gone! Is it true????'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261963288103747645/koishi-farewell-0003.png',
        IMAGE_CREATOR,
        (lambda target: f'My Sun, my Sun tell me where did {target} go...'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261963289664159839/koishi-farewell-0004.png',
        IMAGE_CREATOR,
        (lambda target: f'I hope {target} won\'t forget me.'),
    ),
)


FAREWELL_STYLE = FarewellStyle(
    NAME,
    ITEMS,
)
