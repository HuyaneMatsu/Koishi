__all__ = ()

from re import compile as re_compile

from hata import BUILTIN_EMOJIS, KOKORO
from hata.ext.slash import Button, Select
from scarletio import IgnoreCaseString, ScarletLock


RATE_LIMIT_RESET_AFTER = 60.0
RATE_LIMIT_SIZE = 90

RATE_LIMIT_LOCK = ScarletLock(KOKORO, RATE_LIMIT_SIZE)

HEADER_RETRY_AFTER = IgnoreCaseString('Retry-After')

CUSTOM_ID_FIND_LEFT_ANIME = 'anilist.find.left.anime'
CUSTOM_ID_FIND_RIGHT_ANIME = 'anilist.find.right.anime'
CUSTOM_ID_FIND_SELECT_ANIME = 'anilist.find.select.anime'

CUSTOM_ID_FIND_LEFT_CHARACTER = 'anilist.find.left.character'
CUSTOM_ID_FIND_RIGHT_CHARACTER = 'anilist.find.right.character'
CUSTOM_ID_FIND_SELECT_CHARACTER = 'anilist.find_select.character'

CUSTOM_ID_FIND_LEFT_MANGA = 'anilist.find.left.manga'
CUSTOM_ID_FIND_RIGHT_MANGA = 'anilist.find.right.manga'
CUSTOM_ID_FIND_SELECT_MANGA = 'anilist.find.select.manga'

CUSTOM_ID_FIND_LEFT_DISABLED = 'anilist.find.left.disabled'
CUSTOM_ID_FIND_RIGHT_DISABLED = 'anilist.find.right.disabled'


ENTRY_PER_PAGE = 25
SUB_ENTRY_PER_PAGE = 5
URL_BASE_CHARACTER = 'https://anilist.co/character/'
URL_BASE_ANIME = 'https://anilist.co/anime/'
URL_BASE_MANGA = 'https://anilist.co/manga/'

DESCRIPTION_LENGTH_MAX = 4000
PARAMETER_LENGTH_MAX = 200


EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']

DECIMAL_RP = re_compile('\d+')


COMPONENT_LEFT_ANIME = Button(
    emoji = EMOJI_LEFT,
    custom_id = CUSTOM_ID_FIND_LEFT_ANIME,
)

COMPONENT_RIGHT_ANIME = Button(
    emoji = EMOJI_RIGHT,
    custom_id = CUSTOM_ID_FIND_RIGHT_ANIME,
)

COMPONENT_SELECT_ANIME = Select(
    None,
    custom_id = CUSTOM_ID_FIND_SELECT_ANIME,
    placeholder = 'Select an anime!',
)


COMPONENT_LEFT_CHARACTER = Button(
    emoji = EMOJI_LEFT,
    custom_id = CUSTOM_ID_FIND_LEFT_CHARACTER,
)

COMPONENT_RIGHT_CHARACTER = Button(
    emoji = EMOJI_RIGHT,
    custom_id = CUSTOM_ID_FIND_RIGHT_CHARACTER,
)

COMPONENT_SELECT_CHARACTER = Select(
    None,
    custom_id = CUSTOM_ID_FIND_SELECT_CHARACTER,
    placeholder = 'Select a character!',
)


COMPONENT_LEFT_MANGA = Button(
    emoji = EMOJI_LEFT,
    custom_id = CUSTOM_ID_FIND_LEFT_MANGA,
)

COMPONENT_RIGHT_MANGA = Button(
    emoji = EMOJI_RIGHT,
    custom_id = CUSTOM_ID_FIND_RIGHT_MANGA,
)

COMPONENT_SELECT_MANGA = Select(
    None,
    custom_id = CUSTOM_ID_FIND_SELECT_MANGA,
    placeholder = 'Select a manga!',
)

COMPONENT_LEFT_DISABLED = Button(
    emoji = EMOJI_LEFT,
    custom_id = CUSTOM_ID_FIND_LEFT_DISABLED,
    enabled = False,
)

COMPONENT_RIGHT_DISABLED = Button(
    emoji = EMOJI_RIGHT,
    custom_id = CUSTOM_ID_FIND_RIGHT_DISABLED,
    enabled = False,
)
