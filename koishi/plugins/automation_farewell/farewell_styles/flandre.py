__all__ = ()

import config
from hata import Locale

from ..farewell_style import FarewellStyle
from ..farewell_style_item import FarewellStyleItem

from .constants import IMAGE_CREATOR


NAME = 'flandre'


ITEMS = (
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261948894028369970/flandre-farewell-0000.png',
        IMAGE_CREATOR,
        (lambda target: f'{target} escaped the basement!!'),
        {
            Locale.indonesian: (lambda target: f'{target} melarikan diri dari ruang bawah tanah!!!')
        },
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971119020179456/flandre-farewell-0001.png',
        IMAGE_CREATOR,
        (lambda target: f'Just broke {target}!!'),
        {
            Locale.indonesian: (lambda target: f'Baru saja melanggar {target}!!!')
        },
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971120119353394/flandre-farewell-0002.png',
        IMAGE_CREATOR,
        (lambda target: f'Pache, did {target} really just vanish under the sun???'),
        {
            Locale.indonesian: (lambda target: f'Pachy, apakah {target} benar-benar lenyap di bawah matahari???')
        },
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971121427714099/flandre-farewell-0003.png',
        IMAGE_CREATOR,
        (lambda target: f'Where is {target} going?'),
        {
            Locale.indonesian: (lambda target: f'Dimana {target} itu bersembunyi?')
        },
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261971122606575616/flandre-farewell-0004.png',
        IMAGE_CREATOR,
        (lambda target: f'{target} isn\'t hiding under my bed anymore.'),
        {
            Locale.indonesian: (lambda target: f'{target} tidak lagi bersembunyi dibawah kasurku lagi.')
        },
    ),
)


FAREWELL_STYLE = FarewellStyle(
    NAME,
    config.FLANDRE_ID,
    ITEMS,
)
