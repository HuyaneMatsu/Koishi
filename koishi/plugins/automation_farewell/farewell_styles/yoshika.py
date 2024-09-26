__all__ = ()

from ..farewell_style import FarewellStyle
from ..farewell_style_item import FarewellStyleItem

from .constants import IMAGE_CREATOR


NAME = 'yoshika'


ITEMS = (
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261992949487505408/yoshika-farewel-0000.png',
        IMAGE_CREATOR,
        (lambda target: f'Recovering from {target} tonight!!'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261992950976483420/yoshika-farewel-0001.png',
        IMAGE_CREATOR,
        (lambda target: f'Taking {target} for a walk.'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261992951823859814/yoshika-farewel-0002.png',
        IMAGE_CREATOR,
        (lambda target: f'Seems {target} perished in the night of the Jiang Shi...'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261992952859984008/yoshika-farewel-0003.png',
        IMAGE_CREATOR,
        (lambda target: f'Looks like {target} went out for a decomposing night!'),
    ),
    FarewellStyleItem(
        'https://cdn.discordapp.com/attachments/568837922288173058/1261992953925341264/yoshika-farewel-0004.png',
        IMAGE_CREATOR,
        (lambda target: f'Taking {target} to the hall of dreams\' great mausoleum.'),
    ),
)


FAREWELL_STYLE = FarewellStyle(
    NAME,
    ITEMS,
)
