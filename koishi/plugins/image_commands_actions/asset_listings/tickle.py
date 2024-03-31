__all__ = ('TOUHOU_ACTION_TICKLE',)

from ...image_handling_core import ImageDetail
from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI, SCARLET_FLANDRE, SCARLET_REMILIA


TOUHOU_ACTION_TICKLE = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220263200050774076/flandre-remilia-tickle-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220263410630004756/koishi-orin-satori-tickle-0000.png',
    ).with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI),
]
