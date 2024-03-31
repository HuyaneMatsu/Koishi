__all__ = ()

from ..image_handling_core import ImageHandlerGroup, ImageHandlerStatic, ImageHandlerWaifuPics

from .asset_listings import (
    TOUHOU_ACTION_FEED, TOUHOU_ACTION_FLUFF, TOUHOU_ACTION_HUG, TOUHOU_ACTION_KISS, TOUHOU_ACTION_KON,
    TOUHOU_ACTION_LICK, TOUHOU_ACTION_LIKE, TOUHOU_ACTION_PAT, TOUHOU_ACTION_POCKY_KISS, TOUHOU_ACTION_POCKY_KISS_SELF
)


IMAGE_HANDLER_PAT = ImageHandlerGroup(ImageHandlerWaifuPics('pat', False), ImageHandlerStatic(TOUHOU_ACTION_PAT))
IMAGE_HANDLER_KISS = ImageHandlerGroup(ImageHandlerWaifuPics('kiss', False), ImageHandlerStatic(TOUHOU_ACTION_KISS))
IMAGE_HANDLER_HUG = ImageHandlerGroup(ImageHandlerWaifuPics('hug', False), ImageHandlerStatic(TOUHOU_ACTION_HUG))
IMAGE_HANDLER_CUDDLE = ImageHandlerWaifuPics('cuddle', False)
IMAGE_HANDLER_LICK = ImageHandlerGroup(ImageHandlerWaifuPics('lick', False), ImageHandlerStatic(TOUHOU_ACTION_LICK))
IMAGE_HANDLER_POKE = ImageHandlerWaifuPics('poke', False)
IMAGE_HANDLER_SLAP = ImageHandlerWaifuPics('slap', False)
IMAGE_HANDLER_SMUG = ImageHandlerWaifuPics('smug', False)
IMAGE_HANDLER_BULLY = ImageHandlerWaifuPics('bully', False)
IMAGE_HANDLER_CRY = ImageHandlerWaifuPics('cry', False)
IMAGE_HANDLER_YEET = ImageHandlerWaifuPics('yeet', False)
IMAGE_HANDLER_BLUSH = ImageHandlerWaifuPics('blush', False)
IMAGE_HANDLER_SMILE = ImageHandlerWaifuPics('smile', False)
IMAGE_HANDLER_WAVE = ImageHandlerWaifuPics('wave', False)
IMAGE_HANDLER_HIGHFIVE = ImageHandlerWaifuPics('highfive', False)
IMAGE_HANDLER_HANDHOLD = ImageHandlerWaifuPics('handhold', False)
IMAGE_HANDLER_NOM = ImageHandlerWaifuPics('nom', False)
IMAGE_HANDLER_BITE = ImageHandlerWaifuPics('bite', False)
IMAGE_HANDLER_GLOMP = ImageHandlerWaifuPics('glomp', False)
IMAGE_HANDLER_KILL = ImageHandlerWaifuPics('kill', False)
IMAGE_HANDLER_HAPPY = ImageHandlerWaifuPics('happy', False)
IMAGE_HANDLER_WINK = ImageHandlerWaifuPics('wink', False)
IMAGE_HANDLER_DANCE = ImageHandlerWaifuPics('dance', False)
IMAGE_HANDLER_CRINGE = ImageHandlerWaifuPics('cringe', False)
IMAGE_HANDLER_KICK = ImageHandlerWaifuPics('kick', False)
IMAGE_HANDLER_FEED = ImageHandlerStatic(TOUHOU_ACTION_FEED)
IMAGE_HANDLER_FLUFF = ImageHandlerStatic(TOUHOU_ACTION_FLUFF)
IMAGE_HANDLER_POCKY = ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS)
IMAGE_HANDLER_POCKY_SELF = ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS_SELF)
IMAGE_HANDLER_LIKE = ImageHandlerStatic(TOUHOU_ACTION_LIKE)
IMAGE_HANDLER_KON = ImageHandlerStatic(TOUHOU_ACTION_KON)
