__all__ = ()

from ...image_handler import ImageHandlerStatic, ImageHandlerWaifuPics
from ...touhou import TOUHOU_ACTION_POCKY_KISS, TOUHOU_ACTION_POCKY_KISS_SELF


IMAGE_HANDLER_PAT = ImageHandlerWaifuPics('pat', False)
IMAGE_HANDLER_KISS = ImageHandlerWaifuPics('kiss', False)
IMAGE_HANDLER_HUG = ImageHandlerWaifuPics('hug', False)
IMAGE_HANDLER_CUDDLE = ImageHandlerWaifuPics('cuddle', False)
IMAGE_HANDLER_LICK = ImageHandlerWaifuPics('lick', False)
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
IMAGE_HANDLE_HANDHOLD = ImageHandlerWaifuPics('handhold', False)
IMAGE_HANDLER_NOM = ImageHandlerWaifuPics('nom', False)
IMAGE_HANDLER_BITE = ImageHandlerWaifuPics('bite', False)
IMAGE_HANDLER_GLOMP = ImageHandlerWaifuPics('glomp', False)
IMAGE_HANDLER_KILL = ImageHandlerWaifuPics('kill', False)
IMAGE_HANDLER_HAPPY = ImageHandlerWaifuPics('happy', False)
IMAGE_HANDLER_WINK = ImageHandlerWaifuPics('wink', False)
IMAGE_HANDLER_DANCE = ImageHandlerWaifuPics('dance', False)
IMAGE_HANDLER_CRINGE = ImageHandlerWaifuPics('cringe', False)
IMAGE_HANDLER_KICK = ImageHandlerWaifuPics('kick', False)
IMAGE_HANDLER_POCKY = ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS)

IMAGE_HANDLER_POCKY_SELF = ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS_SELF)
