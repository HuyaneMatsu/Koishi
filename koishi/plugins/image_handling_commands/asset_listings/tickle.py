__all__ = ('TOUHOU_ACTION_TICKLE',)

from ...image_handling_core import ImageDetail
from ...touhou_core.characters import KOMEIJI_KOISHI, KOMEIJI_SATORI, SCARLET_FLANDRE, SCARLET_REMILIA


TOUHOU_ACTION_TICKLE = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023271479024037928/remilia-flandre-tickle-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023272153816244325/koishi-satori-orin-tickle.png',
    ).with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI),
]
