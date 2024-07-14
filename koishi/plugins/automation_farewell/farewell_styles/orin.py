__all__ = ()

from ..farewell_style import FarewellStyle
from ..farewell_style_item import FarewellStyleItem

from .constants import IMAGE_CREATOR


NAME = 'orin'


ITEMS = (
    FarewellStyleItem(
        (lambda target: f'Bad wabbit {target} comes with me miau :3'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261948896393957477/orin-farewell-0000.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'{target} joined my collection!'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261964907125936190/orin-farewell-0001.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'Carting {target} to the hell of blazing fires...'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261964908531155005/orin-farewell-0002.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'It wasn\'t me who carted {target}!!'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261964909965738025/orin-farewell-0003.png',
        IMAGE_CREATOR,
    ),
    FarewellStyleItem(
        (lambda target: f'Oh look, a {target} corpse waiting to be carted! :3'),
        'https://cdn.discordapp.com/attachments/568837922288173058/1261964910959656960/orin-farewell-0004.png',
        IMAGE_CREATOR,
    ),
)


FAREWELL_STYLE = FarewellStyle(
    NAME,
    ITEMS,
)
