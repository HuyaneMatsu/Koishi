__all__ = ()

from hata import BUILTIN_EMOJIS, Color


EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_TAGS = BUILTIN_EMOJIS['notepad_spiral']


SAFE_TAGS_BANNED = frozenset((
    'bdsm',
    'huge_filesize',
    'underwear',
    'sideboob',
    'pov_feet',
    'underboob',
    'upskirt',
    'sexually_suggestive',
    'ass',
    'bikini',
    'clothed_female_nude_male',
    'no_panties',
    'artificial_vagina',
    'covering_breasts',
    'huge_breasts',
    'blood',
    'penetration_gesture',
    'no_bra',
    'nude',
    'butt_crack',
    'naked_apron',
    'pantyshot',
    'open_shirt',
    'clothes_lift',
))


TOUHOU_TAGS_BANNED = frozenset((
    *SAFE_TAGS_BANNED,
    'comic',
    'greyscale',
    'ronald_mcdonald',
))


NSFW_TAGS_BANNED = frozenset((
    'loli',
    'lolicon',
    'shota',
    'shotacon',
    'huge_filesize',
))


SOLO_REQUIRED_TAGS = frozenset((
    'solo',
))


SAFE_BOORU_ENDPOINT = 'http://safebooru.org'
SAFE_BOORU_PROVIDER = 'safebooru'

NSFW_BOORU_ENDPOINT = 'http://gelbooru.com'
NSFW_BOORU_PROVIDER = 'gelbooru'


BOORU_COLOR = Color(0x138a50)
TOUHOU_COLOR = Color(0xffc0dd)
VOCALOID_COLOR = Color(0xc8a96e)
WAIFU_COLOR = Color(0xa96ec8)
