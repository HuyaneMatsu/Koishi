__all__ = ('TOUHOU_ACTION_KISS',)

from ...image_handler import ImageDetail

from ..character import freeze
from ..characters import KOMEIJI_KOISHI, SCARLET_FLANDRE


TOUHOU_ACTION_KISS = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023273826672463873/koishi-flandre-kiss-0000.png',
        freeze(KOMEIJI_KOISHI, SCARLET_FLANDRE),
    ),
]
