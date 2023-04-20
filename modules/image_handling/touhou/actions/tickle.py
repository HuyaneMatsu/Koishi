__all__ = ('TOUHOU_ACTION_TICKLE',)

from ...image_handler import ImageDetail

from ..character import freeze
from ..characters import KOMEIJI_KOISHI, KOMEIJI_SATORI, SCARLET_FLANDRE, SCARLET_REMILIA


TOUHOU_ACTION_TICKLE = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023271479024037928/remilia-flandre-tickle-0000.png',
        freeze(SCARLET_REMILIA, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023272153816244325/koishi-satori-orin-tickle.png',
        freeze(KOMEIJI_KOISHI, KOMEIJI_SATORI),
    ),
]
