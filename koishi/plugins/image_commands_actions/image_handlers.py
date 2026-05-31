__all__ = ()

from ..image_handling_core import ImageHandlerGroup, ImageHandlerWaifuPics
from .asset_listings import (
    TOUHOU_ACTION_BITE, TOUHOU_ACTION_BLUSH, TOUHOU_ACTION_BULLY, TOUHOU_ACTION_CARRY, TOUHOU_ACTION_CRY,
    TOUHOU_ACTION_FEED, TOUHOU_ACTION_FLUFF, TOUHOU_ACTION_HANDHOLD, TOUHOU_ACTION_HAPPY, TOUHOU_ACTION_HUG,
    TOUHOU_ACTION_KISS, TOUHOU_ACTION_KON, TOUHOU_ACTION_LAP_SLEEP, TOUHOU_ACTION_LICK, TOUHOU_ACTION_LIKE,
    TOUHOU_ACTION_MOON, TOUHOU_ACTION_MURDER, TOUHOU_ACTION_NOM, TOUHOU_ACTION_PAT, TOUHOU_ACTION_PEG,
    TOUHOU_ACTION_POCKY_KISS, TOUHOU_ACTION_POCKY_KISS_SELF, TOUHOU_ACTION_POKE, TOUHOU_ACTION_SMUG,
    TOUHOU_ACTION_STARE, TOUHOU_ACTION_WAVE, TOUHOU_ACTION_WINK
)


IMAGE_HANDLER_BITE = ImageHandlerGroup(
    ImageHandlerWaifuPics('bite', True),
    TOUHOU_ACTION_BITE,
)
IMAGE_HANDLER_BLUSH = ImageHandlerGroup(
    ImageHandlerWaifuPics('blush', True),
    TOUHOU_ACTION_BLUSH,
)
IMAGE_HANDLER_BULLY = ImageHandlerGroup(
    ImageHandlerWaifuPics('bully', True),
    TOUHOU_ACTION_BULLY,
)
IMAGE_HANDLER_CARRY = TOUHOU_ACTION_CARRY
IMAGE_HANDLER_CRINGE = ImageHandlerWaifuPics('cringe', True)
IMAGE_HANDLER_CRY = ImageHandlerGroup(
    ImageHandlerWaifuPics('cry', True),
    TOUHOU_ACTION_CRY,
)
IMAGE_HANDLER_CUDDLE = ImageHandlerWaifuPics('cuddle', True)
IMAGE_HANDLER_DANCE = ImageHandlerWaifuPics('dance', True)
IMAGE_HANDLER_FEED = TOUHOU_ACTION_FEED
IMAGE_HANDLER_FLUFF = TOUHOU_ACTION_FLUFF
IMAGE_HANDLER_GLOMP = ImageHandlerWaifuPics('glomp', True)
IMAGE_HANDLER_HANDHOLD = ImageHandlerGroup(
    ImageHandlerWaifuPics('handhold', True),
    TOUHOU_ACTION_HANDHOLD,
)
IMAGE_HANDLER_HAPPY = ImageHandlerGroup(
    ImageHandlerWaifuPics('happy', True),
    TOUHOU_ACTION_HAPPY,
)
IMAGE_HANDLER_HIGHFIVE = ImageHandlerWaifuPics('highfive', True)
IMAGE_HANDLER_HUG = ImageHandlerGroup(
    ImageHandlerWaifuPics('hug', True),
    TOUHOU_ACTION_HUG,
)
IMAGE_HANDLER_KICK = ImageHandlerWaifuPics('kick', True)
IMAGE_HANDLER_KISS = ImageHandlerGroup(
    ImageHandlerWaifuPics('kiss', True),
    TOUHOU_ACTION_KISS,
)
IMAGE_HANDLER_KON = TOUHOU_ACTION_KON
IMAGE_HANDLER_LAP_SLEEP = TOUHOU_ACTION_LAP_SLEEP
IMAGE_HANDLER_LICK = ImageHandlerGroup(
    ImageHandlerWaifuPics('lick', True),
    TOUHOU_ACTION_LICK,
)
IMAGE_HANDLER_LIKE = TOUHOU_ACTION_LIKE
IMAGE_HANDLER_MOON = TOUHOU_ACTION_MOON
IMAGE_HANDLER_MURDER = ImageHandlerGroup(
    ImageHandlerWaifuPics('kill', True),
    TOUHOU_ACTION_MURDER,
)
IMAGE_HANDLER_NOM = ImageHandlerGroup(
    ImageHandlerWaifuPics('nom', True),
    TOUHOU_ACTION_NOM,
)
IMAGE_HANDLER_PAT = ImageHandlerGroup(
    ImageHandlerWaifuPics('pat', True),
    TOUHOU_ACTION_PAT,
)
IMAGE_HANDLER_PEG = TOUHOU_ACTION_PEG
IMAGE_HANDLER_POCKY_KISS = TOUHOU_ACTION_POCKY_KISS
IMAGE_HANDLER_POCKY_KISS_SELF = TOUHOU_ACTION_POCKY_KISS_SELF
IMAGE_HANDLER_POKE = ImageHandlerGroup(
    ImageHandlerWaifuPics('poke', True),
    TOUHOU_ACTION_POKE,
)
IMAGE_HANDLER_SLAP = ImageHandlerWaifuPics('slap', True)
IMAGE_HANDLER_SMILE = ImageHandlerWaifuPics('smile', True)
IMAGE_HANDLER_SMUG = ImageHandlerGroup(
    ImageHandlerWaifuPics('smug', True),
    TOUHOU_ACTION_SMUG,
)
IMAGE_HANDLER_STARE = TOUHOU_ACTION_STARE
IMAGE_HANDLER_WAVE = ImageHandlerGroup(
    ImageHandlerWaifuPics('wave', True),
    TOUHOU_ACTION_WAVE,
)
IMAGE_HANDLER_WINK = ImageHandlerGroup(
    ImageHandlerWaifuPics('wink', True),
    TOUHOU_ACTION_WINK,
)
IMAGE_HANDLER_YEET = ImageHandlerWaifuPics('yeet', True)
