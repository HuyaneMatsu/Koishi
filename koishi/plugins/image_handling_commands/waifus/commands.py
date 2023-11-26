__all__ = ()

from itertools import chain

from ....bots import FEATURE_CLIENTS

from .waifu import Waifu



SAFE_WAIFU_TYPES = [
    'waifu',
    'neko',
    'awoo',
    'shinobu',
    'megumin',
]

NSFW_WAIFU_TYPES = [
    'waifu',
    'neko',
    'trap',
]

SAFE_HANDLERS = {waifu_type: Waifu(waifu_type, False) for waifu_type in SAFE_WAIFU_TYPES}
NSFW_HANDLERS = {waifu_type: Waifu(waifu_type, True ) for waifu_type in NSFW_WAIFU_TYPES}


@FEATURE_CLIENTS.interactions(is_global = True)
async def waifu_safe(
    client,
    event,
    type_ : (SAFE_WAIFU_TYPES, 'Waifu type!') = SAFE_WAIFU_TYPES[0],
):
    """Safe working waifu."""
    await SAFE_HANDLERS[type_](client, event)


@FEATURE_CLIENTS.interactions(is_global = True, nsfw = True)
async def waifu_nsfw(
    client,
    event,
    type_ : (NSFW_WAIFU_TYPES, 'Waifu type!') = NSFW_WAIFU_TYPES[0],
):
    """Waifu with extras!"""
    await NSFW_HANDLERS[type_](client, event)



for waifu in chain(SAFE_HANDLERS.values(), NSFW_HANDLERS.values()):
    FEATURE_CLIENTS.interactions(waifu.get_renew_command(), custom_id = waifu.custom_id)

waifu = None
del waifu
