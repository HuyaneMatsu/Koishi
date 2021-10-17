from re import compile as re_compile, U as re_unicode, M as re_multi_line, S as re_dotall
from hata import Client, to_json, Embed, istr, KOKORO, sleep, ScarletLock, BUILTIN_EMOJIS
from hata.backend.headers import CONTENT_TYPE
from hata.ext.slash import abort, Row, Button, InteractionResponse, Select, Option
from collections import namedtuple as NamedTupleType

from bot_utils.constants import GUILD__NEKO_DUNGEON

SLASH_CLIENT: Client

RATE_LIMIT_RESET_AFTER = 60.0
RATE_LIMIT_SIZE = 90

RATE_LIMIT_LOCK = ScarletLock(KOKORO, RATE_LIMIT_SIZE)

RETRY_AFTER = istr('Retry-After')

CUSTOM_ID_FIND_CHARACTER_LEFT = 'anilist.find_character.l'
CUSTOM_ID_FIND_CHARACTER_RIGHT = 'anilist.find_character.r'
CUSTOM_ID_FIND_CHARACTER_SELECT = 'anilist.find_character.s'
CUSTOM_ID_FIND_CHARACTER_LEFT_DISABLED = 'anilist.find_character._.0'
CUSTOM_ID_FIND_CHARACTER_RIGHT_DISABLED = 'anilist.find_character._.1'
CUSTOM_ID_FIND_CHARACTER_SELECT_DISABLED = 'anilist.find_character._.2'
CUSTOM_ID_FIND_ANIME_LEFT = 'anilist.find_anime.l'
CUSTOM_ID_FIND_ANIME_RIGHT = 'anilist.find_anime.r'
CUSTOM_ID_FIND_ANIME_SELECT = 'anilist.find_anime.s'
CUSTOM_ID_FIND_ANIME_LEFT_DISABLED = 'anilist.find_anime._.0'
CUSTOM_ID_FIND_ANIME_RIGHT_DISABLED = 'anilist.find_anime._.1'
CUSTOM_ID_FIND_ANIME_SELECT_DISABLED = 'anilist.find_anime._.2'
CUSTOM_ID_FIND_MANGA_LEFT = 'anilist.find_manga.l'
CUSTOM_ID_FIND_MANGA_RIGHT = 'anilist.find_manga.r'
CUSTOM_ID_FIND_MANGA_SELECT = 'anilist.find_manga.s'
CUSTOM_ID_FIND_MANGA_LEFT_DISABLED = 'anilist.find_manga._.0'
CUSTOM_ID_FIND_MANGA_RIGHT_DISABLED = 'anilist.find_manga._.1'
CUSTOM_ID_FIND_MANGA_SELECT_DISABLED = 'anilist.find_manga._.2'

ENTRY_PER_PAGE = 25
SUB_ENTRY_PER_PAGE = 5
URL_BASE_CHARACTER = 'https://anilist.co/character/'
URL_BASE_ANIME = 'https://anilist.co/anime/'
URL_BASE_MANGA = 'https://anilist.co/manga/'

SELECT_FIND_CHARACTER_NO_RESULT = Select(
    [Option('_', 'No result', default=True)],
    CUSTOM_ID_FIND_CHARACTER_SELECT_DISABLED,
    placeholder = 'No result',
)


EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']

DECIMAL_RP = re_compile('\d+')

KEY_CHARACTER = 'Character'
KEY_CHARACTER_ARRAY = 'characters'
KEY_MEDIA = 'Media'
KEY_MEDIA_ARRAY = 'media'

KEY_PAGE = 'Page'
KEY_PAGE_INFO = 'pageInfo'
KEY_PAGE_INFO_TOTAL_ENTRIES = 'total'
KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER = 'currentPage'
KEY_PAGE_INFO_TOTAL_PAGES = 'lastPage'

KEY_CHARACTER_SITE_URL = 'siteUrl'
KEY_CHARACTER_NAME = 'name'
KEY_CHARACTER_NAME_FIRST = 'last'
KEY_CHARACTER_NAME_MIDDLE = 'middle'
KEY_CHARACTER_NAME_LAST = 'first'
KEY_CHARACTER_NAME_NATIVE = 'native'
KEY_CHARACTER_NAME_ALTERNATIVE = 'alternative'
KEY_CHARACTER_NAME_ALTERNATIVE_SPOILER = 'alternativeSpoiler'
KEY_CHARACTER_NAME_USER_PREFERRED = 'userPreferred'
KEY_CHARACTER_NAME_FULL = 'full'
KEY_CHARACTER_DESCRIPTION = 'description'
KEY_CHARACTER_IMAGE = 'image'
KEY_CHARACTER_IMAGE_LARGE = 'large'
KEY_CHARACTER_ID = 'id'
KEY_CHARACTER_FAVOURITES = 'favourites'
KEY_CHARACTER_BIRTH_DATE = 'dateOfBirth'
KEY_CHARACTER_GENDER = 'gender'
KEY_CHARACTER_BLOOD_TYPE = 'bloodType'
KEY_CHARACTER_AGE = 'age'
KEY_CHARACTER_MEDIA_CONNECTIONS = 'media'
KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY = 'nodes'

KEY_MEDIA_TYPE = 'type'
KEY_MEDIA_TYPE_ANIME = 'ANIME'
KEY_MEDIA_TYPE_MANGA = 'MANGA'
KEY_MEDIA_ID = 'id'
KEY_MEDIA_NAME = 'title'
KEY_MEDIA_NAME_ROMAJI = 'romaji'
KEY_MEDIA_NAME_ROMAJI_MODIFIER = 'stylised:false'
KEY_MEDIA_NAME_NATIVE = 'native'
KEY_MEDIA_NAME_NATIVE_MODIFIER = 'stylised:false'
KEY_MEDIA_DESCRIPTION = 'description'
KEY_MEDIA_DESCRIPTION_MODIFIER = 'asHtml:false'
KEY_MEDIA_EPISODE_COUNT = 'episodes'
KEY_MEDIA_FORMAT = 'format'
KEY_MEDIA_RELEASE_SEASON = 'season'
KEY_MEDIA_STATUS = 'status'
KEY_MEDIA_STATUS_MODIFIER = 'version:2'
KEY_MEDIA_EPISODE_LENGTH = 'duration'
KEY_MEDIA_SITE_URL = 'siteUrl'
KEY_MEDIA_START_DATE = 'startDate'
KEY_MEDIA_END_DATE = 'endDate'
KEY_MEDIA_BANNER_IMAGE = 'bannerImage'
KEY_MEDIA_GENRES = 'genres'
KEY_MEDIA_AVERAGE_SCORE = 'averageScore'
KEY_MEDIA_IMAGE = 'coverImage'
KEY_MEDIA_IMAGE_LARGE = 'large'
KEY_MEDIA_CHAPTER_COUNT = 'chapters'
KEY_MEDIA_VOLUME_COUNT = 'volumes'

KEY_FUZZY_DATE_YEAR = 'year'
KEY_FUZZY_DATE_MONTH = 'month'
KEY_FUZZY_DATE_DAY = 'day'

KEY_QUERY = 'query'
KEY_VARIABLES = 'variables'
KEY_PER_PAGE = 'perPage'
KEY_PAGE_IDENTIFIER = 'page'
KEY_SEARCH = 'search'

KEY_VARIABLE_CHARACTER_QUERY = 'query'
KEY_VARIABLE_CHARACTER_ID = 'id'

KEY_VARIABLE_MEDIA_QUERY = 'query'
KEY_VARIABLE_MEDIA_ID = 'id'

KEY_VARIABLE_PER_PAGE = 'per_page'
KEY_VARIABLE_PAGE_IDENTIFIER = 'page'


REQUIRED_CHARACTER_FIELDS = (
    f'{KEY_CHARACTER_ID} '
    f'{KEY_CHARACTER_NAME}{{'
        f'{KEY_CHARACTER_NAME_FIRST} '
        f'{KEY_CHARACTER_NAME_MIDDLE} '
        f'{KEY_CHARACTER_NAME_LAST} '
        f'{KEY_CHARACTER_NAME_NATIVE}'
    f'}}'
    f'{KEY_CHARACTER_IMAGE}{{'
        f'{KEY_CHARACTER_IMAGE_LARGE}'
    f'}}'
    f'{KEY_CHARACTER_BIRTH_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_CHARACTER_DESCRIPTION} '
    f'{KEY_CHARACTER_GENDER} '
    f'{KEY_CHARACTER_BLOOD_TYPE} '
    f'{KEY_CHARACTER_AGE} '
    f'{KEY_CHARACTER_MEDIA_CONNECTIONS}('
        f'sort:[POPULARITY_DESC],'
        f'{KEY_PER_PAGE}:{SUB_ENTRY_PER_PAGE}'
    f'){{'
        f'{KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY}{{'
            f'{KEY_MEDIA_ID} '
            f'{KEY_MEDIA_TYPE} '
            f'{KEY_MEDIA_NAME}{{'
                f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
            f'}}'
        f'}}'
    f'}}'
)


QUERY_CHARACTER = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_QUERY}:String){{'
        f'{KEY_CHARACTER}({KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)

QUERY_CHARACTER_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_ID}:Int){{'
        f'{KEY_CHARACTER}({KEY_CHARACTER_ID}: ${KEY_VARIABLE_CHARACTER_ID}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)

QUERY_CHARACTER_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_TOTAL_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER} '
                f'{KEY_PAGE_INFO_TOTAL_PAGES}'
            f'}}'
            f'{KEY_CHARACTER_ARRAY}({KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}){{'
                f'{KEY_CHARACTER_ID} '
                f'{KEY_CHARACTER_NAME}{{'
                    f'{KEY_CHARACTER_NAME_FIRST} '
                    f'{KEY_CHARACTER_NAME_MIDDLE} '
                    f'{KEY_CHARACTER_NAME_LAST} '
                    f'{KEY_CHARACTER_NAME_NATIVE}'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)


REQUIRED_ANIME_FIELDS = (
    f'{KEY_MEDIA_ID} '
    f'{KEY_MEDIA_NAME}{{'
        f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
        f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
    f'}}'
    f'{KEY_MEDIA_DESCRIPTION}({KEY_MEDIA_DESCRIPTION_MODIFIER})'
    f'{KEY_MEDIA_EPISODE_COUNT} '
    f'{KEY_MEDIA_FORMAT} '
    f'{KEY_MEDIA_STATUS}({KEY_MEDIA_STATUS_MODIFIER})'
    f'{KEY_MEDIA_EPISODE_LENGTH} '
    f'{KEY_MEDIA_START_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_END_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_IMAGE}{{'
        f'{KEY_MEDIA_IMAGE_LARGE}'
    f'}}'
    f'{KEY_MEDIA_GENRES} '
    f'{KEY_MEDIA_AVERAGE_SCORE}'
)


QUERY_ANIME = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_QUERY}:String){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},{KEY_SEARCH}:${KEY_VARIABLE_MEDIA_QUERY}){{'
            f'{REQUIRED_ANIME_FIELDS}'
        f'}}'
    f'}}'
)

QUERY_ANIME_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_ID}:Int){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},{KEY_MEDIA_ID}:${KEY_VARIABLE_MEDIA_ID}){{'
            f'{REQUIRED_ANIME_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_ANIME_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_TOTAL_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER} '
                f'{KEY_PAGE_INFO_TOTAL_PAGES}'
            f'}}'
            f'{KEY_MEDIA_ARRAY}('
                f'{KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},'
                f'{KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}'
            f'){{'
                f'{KEY_MEDIA_ID} '
                f'{KEY_MEDIA_NAME}{{'
                    f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                    f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)


REQUIRED_MANGA_FIELDS = (
    f'{KEY_MEDIA_ID} '
    f'{KEY_MEDIA_NAME}{{'
        f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
        f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
    f'}}'
    f'{KEY_MEDIA_DESCRIPTION}({KEY_MEDIA_DESCRIPTION_MODIFIER})'
    f'{KEY_MEDIA_VOLUME_COUNT} '
    f'{KEY_MEDIA_FORMAT} '
    f'{KEY_MEDIA_STATUS}({KEY_MEDIA_STATUS_MODIFIER})'
    f'{KEY_MEDIA_CHAPTER_COUNT} '
    f'{KEY_MEDIA_START_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_END_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_IMAGE}{{'
        f'{KEY_MEDIA_IMAGE_LARGE}'
    f'}}'
    f'{KEY_MEDIA_GENRES} '
    f'{KEY_MEDIA_AVERAGE_SCORE}'
)


QUERY_MANGA = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_QUERY}:String){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},{KEY_SEARCH}:${KEY_VARIABLE_MEDIA_QUERY}){{'
            f'{REQUIRED_MANGA_FIELDS}'
        f'}}'
    f'}}'
)

QUERY_MANGA_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_ID}:Int){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},{KEY_MEDIA_ID}:${KEY_VARIABLE_MEDIA_ID}){{'
            f'{REQUIRED_MANGA_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_MANGA_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_TOTAL_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER} '
                f'{KEY_PAGE_INFO_TOTAL_PAGES}'
            f'}}'
            f'{KEY_MEDIA_ARRAY}('
                f'{KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},'
                f'{KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}'
            f'){{'
                f'{KEY_MEDIA_ID} '
                f'{KEY_MEDIA_NAME}{{'
                    f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                    f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)


MEDIA_FORMAT_MAP = {
    'TV': 'tv',
    'TV_SHORT': 'tv short',
    'MOVIE': 'movie',
    'SPECIAL': 'special',
    'OVA': 'ova',
    'ONA': 'ona',
    'MUSIC': 'music',
    'MANGA': 'manga',
    'NOVEL': 'novel',
    'ONE_SHOT': 'one shot'
}


def convert_media_format(media_format):
    try:
        converted_media_format = MEDIA_FORMAT_MAP[media_format]
    except KeyError:
        converted_media_format = media_format.lower().replace('_', ' ')
        MEDIA_FORMAT_MAP[media_format] = converted_media_format
    
    return converted_media_format


MEDIA_STATUS_MAP = {
    'FINISHED': 'finished',
    'RELEASING': 'releasing',
    'NOT_YET_RELEASED': 'not yet released',
    'CANCELLED': 'cancelled',
    'HIATUS': 'hiatus',
}


def convert_media_status(media_status):
    try:
        converted_media_status = MEDIA_STATUS_MAP[media_status]
    except KeyError:
        converted_media_status = media_status.lower().replace('_', ' ')
        MEDIA_STATUS_MAP[media_status] = converted_media_status
    
    return converted_media_status


def build_media_name(media_data):
    name_data = media_data[KEY_MEDIA_NAME]
    name_romaji = name_data[KEY_MEDIA_NAME_ROMAJI]
    name_native = name_data[KEY_MEDIA_NAME_NATIVE]
    
    if (name_romaji is None):
        if (name_native is None):
            name = '???'
        else:
            name = name_native
    else:
        if (name_native is None) or (name_romaji == name_native):
            name = name_romaji
        else:
            name = f'{name_romaji} ({name_native})'
    
    return name


def build_character_name(character_data):
    name_data = character_data[KEY_CHARACTER_NAME]
    name_first = name_data[KEY_CHARACTER_NAME_FIRST]
    name_middle = name_data[KEY_CHARACTER_NAME_MIDDLE]
    name_last = name_data[KEY_CHARACTER_NAME_LAST]
    name_native = name_data[KEY_CHARACTER_NAME_NATIVE]
    
    name_parts = []
    
    if (name_first is not None):
        name_parts.append(name_first)
        
        field_added = True
    else:
        field_added = False
    
    if (name_middle is not None):
        if field_added:
            name_parts.append(' ')
        else:
            field_added = True
        
        name_parts.append(name_middle)
    
    if (name_last is not None):
        if field_added:
            name_parts.append(' ')
        else:
            field_added = True
        
        name_parts.append(name_last)
    
    if (name_native is not None):
        if field_added:
            name_parts.append(' (')
        
        name_parts.append(name_native)
        
        if field_added:
            name_parts.append(')')
    
    return ''.join(name_parts)


ArrayResponseBuilderWorkSetType = NamedTupleType(
    'ComponentWorkSetType',
    (
        'button_left',
        'button_left_disabled',
        'button_right',
        'button_right_disabled',
        'select_disabled',
        'select_custom_id',
        'select_placeholder',
        'name_builder',
        'key_id',
        'key_array',
    )
)

ARRAY_WORK_SET_CHARACTER = ArrayResponseBuilderWorkSetType(
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_CHARACTER_LEFT,
    ),
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_CHARACTER_LEFT_DISABLED,
        enabled = False,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_CHARACTER_RIGHT,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_CHARACTER_RIGHT_DISABLED,
        enabled = False,
    ),
    Select(
        [Option('_', 'No result', default=True)],
        CUSTOM_ID_FIND_CHARACTER_SELECT_DISABLED,
        placeholder = 'No result',
    ),
    CUSTOM_ID_FIND_CHARACTER_SELECT,
    'Select a character!',
    build_character_name,
    KEY_CHARACTER_ID,
    KEY_CHARACTER_ARRAY,
)

ARRAY_WORK_SET_ANIME = ArrayResponseBuilderWorkSetType(
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_ANIME_LEFT,
    ),
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_ANIME_LEFT_DISABLED,
        enabled = False,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_ANIME_RIGHT,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_ANIME_RIGHT_DISABLED,
        enabled = False,
    ),

    Select(
        [Option('_', 'No result', default=True)],
        CUSTOM_ID_FIND_ANIME_SELECT_DISABLED,
        placeholder = 'No result',
    ),
    CUSTOM_ID_FIND_ANIME_SELECT,
    'Select an anime!',
    build_media_name,
    KEY_MEDIA_ID,
    KEY_MEDIA_ARRAY,
)

ARRAY_WORK_SET_MANGA = ArrayResponseBuilderWorkSetType(
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_MANGA_LEFT,
    ),
    Button(
        emoji = EMOJI_LEFT,
        custom_id = CUSTOM_ID_FIND_MANGA_LEFT,
        enabled = False,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_MANGA_RIGHT,
    ),
    Button(
        emoji = EMOJI_RIGHT,
        custom_id = CUSTOM_ID_FIND_MANGA_RIGHT_DISABLED,
        enabled = False,
    ),
    Select(
        [Option('_', 'No result', default=True)],
        CUSTOM_ID_FIND_MANGA_SELECT_DISABLED,
        placeholder = 'No result',
    ),
    CUSTOM_ID_FIND_MANGA_SELECT,
    'Select a manga!',
    build_media_name,
    KEY_MEDIA_ID,
    KEY_MEDIA_ARRAY,
)


MONTH_NAMES_SHORT = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec',
}

MONTH_NAMES_FULL = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


def build_fuzzy_date(date_data):
    fuzzy_date_year = date_data[KEY_FUZZY_DATE_YEAR]
    fuzzy_date_month = date_data[KEY_FUZZY_DATE_MONTH]
    fuzzy_date_day = date_data[KEY_FUZZY_DATE_DAY]

    if (fuzzy_date_year is not None) or (fuzzy_date_month is not None) or (fuzzy_date_day is not None):
        date_value_parts = []
        if fuzzy_date_year is None:
            if (fuzzy_date_month is None):
                fuzzy_date_day_value = str(fuzzy_date_day)
                date_value_parts.append(fuzzy_date_day_value)
                date_value_parts.append(' (day of month)')
            else:
                if (fuzzy_date_day is None):
                    fuzzy_date_month_value = MONTH_NAMES_FULL.get(fuzzy_date_month, '???')
                    date_value_parts.append(fuzzy_date_month_value)
                else:
                    fuzzy_date_month_value = MONTH_NAMES_SHORT.get(fuzzy_date_month, '???')
                    fuzzy_date_day_value = str(fuzzy_date_day)
                    date_value_parts.append(fuzzy_date_month_value)
                    date_value_parts.append(' ')
                    date_value_parts.append(fuzzy_date_day_value)
        else:
            fuzzy_date_year_value = str(fuzzy_date_year)
            date_value_parts.append(fuzzy_date_year_value)
            if (fuzzy_date_month is None):
                if (fuzzy_date_day is None):
                    date_value_parts.append(' (year)')
                else:
                    fuzzy_date_day_value = str(fuzzy_date_day)
                    date_value_parts.append('-??-')
                    date_value_parts.append(fuzzy_date_day_value)
            else:
                fuzzy_date_month_value = str(fuzzy_date_month)
                date_value_parts.append('-')
                date_value_parts.append(fuzzy_date_month_value)
                date_value_parts.append('-')
                
                if (fuzzy_date_day is None):
                    fuzzy_date_day_value = '??'
                else:
                    fuzzy_date_day_value = str(fuzzy_date_day)
                
                date_value_parts.append(fuzzy_date_day_value)
        
        date_value = ''.join(date_value_parts)
    else:
        date_value = None
    
    return date_value


DESCRIPTION_RP = re_compile(
    (
        '~!|' # Spoiler tag
        '!~|' # Spoiler tag ending
        '__|' # bold
        ' \(\d+\'(?:\d+\")?\)|' # US shit
        '<br>(?:<br>)?|' # They don't know what not html format means
        '&#039|' # They don't know what not html format means
        '</?i>' # They don't know what not html format means
    ),
    re_multi_line|re_unicode|re_dotall,
)

DESCRIPTION_RELATION = {
    '~!': '||',
    '!~': '||',
    '__': '**',
    '<br><br>': '\n',
    '<br>': '\n',
    '&#039': '\'',
    '<i>': '*',
    '</i>': '*',
}

def DESCRIPTION_REPLACER(match):
    return DESCRIPTION_RELATION.get(match.group(0), '')


def validate_parameter(parameter):
    if len(parameter) > 200:
        parameter = parameter[:200]
    
    return parameter


def build_character_description(character_data):
    description = character_data[KEY_CHARACTER_DESCRIPTION]
    gender = character_data[KEY_CHARACTER_GENDER]
    blood_type = character_data[KEY_CHARACTER_BLOOD_TYPE]
    age = character_data[KEY_CHARACTER_AGE]
    
    description_parts = []
    
    birth_date_value = build_fuzzy_date(character_data[KEY_CHARACTER_BIRTH_DATE])
    if (birth_date_value is not None):
        description_parts.append('**Birthday:** ')
        description_parts.append(birth_date_value)
        
        field_added = True
    else:
        field_added = False
    
    if (age is not None):
        if field_added:
            description_parts.append('\n')
        else:
            field_added = True
        
        description_parts.append('**Age:** ')
        description_parts.append(age)
    
    if (gender is not None):
        if field_added:
            description_parts.append('\n')
        else:
            field_added = True
        
        description_parts.append('**Gender:** ')
        description_parts.append(gender)
    
    if (blood_type is not None):
        if field_added:
            description_parts.append('\n')
        else:
            field_added = True
        
        description_parts.append('**Blood type:** ')
        description_parts.append(blood_type)
    
    if (description is not None) and description:
        description = DESCRIPTION_RP.sub(DESCRIPTION_REPLACER, description)
        
        if field_added:
            if description.startswith('**'):
                description_parts.append('\n')
            elif description.startswith('\n**'):
                pass
            else:
                description_parts.append('\n\n')
        
        description_parts.append(description)
    
    description = ''.join(description_parts)
    
    if len(description) > 4000:
        description = description[:4000]+'...'
    
    return description

TEXT_RELATED_MEDIAS = 'Related medias'
TEXT_RELATED_MEDIAS_TOP_N = f'Related medias (top {SUB_ENTRY_PER_PAGE})'

def add_media_connection_field(embed, character_data):
    media_array = character_data[KEY_CHARACTER_MEDIA_CONNECTIONS][KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY]
    
    if (media_array is None) or (not media_array):
        return
        
    description_parts = []
    
    array_index = 0
    array_limit = len(media_array)
    
    while True:
        media_data = media_array[array_index]
        array_index += 1
        
        media_name = build_media_name(media_data)
        media_id = media_data[KEY_MEDIA_ID]
        
        media_type = media_data[KEY_MEDIA_TYPE]
        if media_type == KEY_MEDIA_TYPE_ANIME:
            url_base = URL_BASE_ANIME
        elif media_type == KEY_MEDIA_TYPE_MANGA:
            url_base = URL_BASE_MANGA
        else:
            url_base = None
        
        if url_base is None:
            description_parts.append(media_name)
        else:
            description_parts.append('[')
            description_parts.append(media_name)
            description_parts.append('](')
            description_parts.append(url_base)
            description_parts.append(str(media_id))
            description_parts.append(')')
        
        if array_index == array_limit:
            break
        
        description_parts.append('\n')
        continue
    
    description = ''.join(description_parts)
    
    if array_limit >= SUB_ENTRY_PER_PAGE:
        title = TEXT_RELATED_MEDIAS_TOP_N
    else:
        title = TEXT_RELATED_MEDIAS
    
    embed.add_field(title, description)


def array_response_builder(data, extra, work_set):
    page_data = data['data'][KEY_PAGE]
    array = page_data[work_set.key_array]
    page_info = page_data[KEY_PAGE_INFO]
    
    array_length = len(array)
    if array_length:
        description_parts = []
        options = []
        
        name_builder = work_set.name_builder
        key_id = work_set.key_id
        
        array_index = 0
        
        while True:
            character_data = array[array_index]
            array_index += 1
            
            name = name_builder(character_data)
            entity_id = character_data[key_id]
            entity_id_str = str(entity_id)
            
            description_parts.append('`')
            description_parts.append(entity_id_str)
            description_parts.append('`: [')
            description_parts.append(name)
            description_parts.append('](')
            description_parts.append(URL_BASE_CHARACTER)
            description_parts.append(entity_id_str)
            description_parts.append(')')
            
            if len(name) > 80:
                name = name[:77]+'...'
            
            options.append(Option(entity_id_str, name))
            if array_index == array_length:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
        select_row = Row(
            Select(
                options,
                work_set.select_custom_id,
                placeholder = work_set.select_placeholder
            ),
        )
    
    else:
        description = 'No result.'
        select_row = work_set.select_disabled
    
    embed = Embed(
        f'Search result for: {extra}',
        description,
    )
    
    total_entries = page_info[KEY_PAGE_INFO_TOTAL_ENTRIES]
    current_page_identifier = page_info[KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER]
    total_pages = page_info[KEY_PAGE_INFO_TOTAL_PAGES]
    
    embed.add_footer(f'Page: {current_page_identifier} / {total_pages} | Total entries: {total_entries}')
    
    if current_page_identifier <= 1:
        button_left = work_set.button_left_disabled
    else:
        button_left = work_set.button_left
    
    if current_page_identifier >= total_pages:
        button_right = work_set.button_right_disabled
    else:
        button_right = work_set.button_right
    
    return InteractionResponse(
        embed = embed,
        components = [
            select_row,
            Row(button_left, button_right),
        ],
    )


async def search(client, json_query, response_builder, extra):
    if RATE_LIMIT_LOCK.locked():
        yield
    
    await RATE_LIMIT_LOCK.acquire()
    
    try:
        while True:
            async with client.http.post(
                'https://graphql.anilist.co',
                {CONTENT_TYPE: 'application/json'},
                data = to_json(json_query),
            ) as response:
                status_code = response.status
                if status_code == 200:
                    data = await response.json()
                    break
                
                elif status_code == 400:
                    raw_data = await response.read()
                    await client.events.error(client, 'anilist.character', raw_data)
                    abort('Something went wrong, please try again later.')
                    return
                
                elif status_code == 429:
                    retry_after = response.headers.get(RETRY_AFTER, None)
                    if (retry_after is None):
                        retry_after = 5
                    
                    yield
                    await sleep(retry_after, KOKORO)
                    continue
                
                elif status_code == 404:
                    data = None
                    break
                
                elif status_code > 500:
                    abort('Internal server error occurred, please try again later.')
                    return
                
                else:
                    raw_data = await response.read()
                    await client.events.error(client,
                        'anilist.character',
                        f'{status_code!r} {response.headers!r} {raw_data}',
                    )
                    abort('Something went wrong, please try again later.')
                    return
            
            if response.status != 200:
                abort(repr(await response.read()))
    finally:
        KOKORO.call_later(RATE_LIMIT_RESET_AFTER, RATE_LIMIT_LOCK.release)
    
    
    yield response_builder(data, extra)


def character_response_builder(data, extra):
    if data is None:
        return Embed(description='No result.')
    
    character_data = data['data'][KEY_CHARACTER]
    
    image_url = character_data[KEY_CHARACTER_IMAGE][KEY_CHARACTER_IMAGE_LARGE]
    url = f'{URL_BASE_CHARACTER}{character_data[KEY_CHARACTER_ID]}'
    
    embed = Embed(
        build_character_name(character_data),
        build_character_description(character_data),
        url = url,
    ).add_thumbnail(
        image_url,
    )
    
    add_media_connection_field(
        embed,
        character_data,
    )
    
    return embed


def character_response_builder_no_components(data, extra):
    embed = character_response_builder(data, extra)
    return InteractionResponse(embed=embed, components=None)


def build_media_description(anime_data):
    description_parts = []
    
    genres = anime_data[KEY_MEDIA_GENRES]
    if (genres is not None) and genres:
        description_parts.append('**Genres**: ')
        genre_index = 0
        genre_limit = len(genres)
        
        while True:
            genre = genres[genre_index]
            genre_index += 1
            
            description_parts.append(genre)
            if genre_index == genre_limit:
                break
            
            description_parts.append(', ')
            continue
        
        field_added = True
    
    else:
        field_added = False
    
    
    description = anime_data[KEY_MEDIA_DESCRIPTION]
    
    if (description is not None) and description:
        if field_added:
            description_parts.append('\n\n')
        else:
            field_added = False
        
        description = DESCRIPTION_RP.sub(DESCRIPTION_REPLACER, description)
        description_parts.append(description)
    
    if field_added:
        description = ''.join(description_parts)
        
        if len(description) > 4000:
            description = description[:4000]+'...'
    else:
        description = None
    
    return description


def add_generic_media_fields(embed, media_data):
    media_status = convert_media_status(media_data[KEY_MEDIA_STATUS])
    embed.add_field('Status', media_status, inline=True)
    
    # line 2
    
    media_format = convert_media_format(media_data[KEY_MEDIA_FORMAT])
    embed.add_field('Format', media_format, inline=True)
    
    start_date_value = build_fuzzy_date(media_data[KEY_MEDIA_START_DATE])
    end_date_value = build_fuzzy_date(media_data[KEY_MEDIA_END_DATE])
    
    if (start_date_value is None):
        if (end_date_value is not None):
            field_name = None
            field_value = None
        else:
            field_name = 'Ended'
            field_value = end_date_value
    else:
        if (end_date_value is None):
            field_name = 'Started'
            field_value = start_date_value
        else:
            if (start_date_value == end_date_value):
                field_name = 'Aired'
                field_value = start_date_value
            else:
                field_name = 'Released'
                field_value = f'Between {start_date_value} and {end_date_value}'
    
    if (field_name is not None):
        embed.add_field(field_name, field_value, inline=True)
    
    average_score = media_data[KEY_MEDIA_AVERAGE_SCORE]
    if (average_score is not None):
        embed.add_field('Average score', f'{average_score} / 100', inline=True)


def build_anime_stat_fields(embed, anime_data):
    
    # Line 1
    
    episode_count = anime_data[KEY_MEDIA_EPISODE_COUNT]
    if (episode_count is not None) and (episode_count != 1):
        embed.add_field('Episodes', str(episode_count), inline=True)
    
    
    episode_length = anime_data[KEY_MEDIA_EPISODE_LENGTH]
    if (episode_length is not None):
        if (episode_count is not None) and (episode_count == 1):
            field_name = 'Length'
        else:
            field_name = 'Episode length'
        
        embed.add_field(field_name, f'{episode_length} minute', inline=True)
    
    add_generic_media_fields(embed, anime_data)


def build_manga_stat_fields(embed, manga_data):
    
    # Line 1
    
    volume_count = manga_data[KEY_MEDIA_VOLUME_COUNT]
    if (volume_count is not None):
        embed.add_field('Volumes', str(volume_count), inline=True)
    
    
    chapter_count = manga_data[KEY_MEDIA_CHAPTER_COUNT]
    if (chapter_count is not None):
        embed.add_field('Chapters', chapter_count, inline=True)
    
    add_generic_media_fields(embed, manga_data)


def anime_response_builder(data, extra):
    if data is None:
        return Embed(description='No result.')
    
    anime_data = data['data'][KEY_MEDIA]
    
    image_url = anime_data[KEY_MEDIA_IMAGE][KEY_MEDIA_IMAGE_LARGE]
    url = f'{URL_BASE_ANIME}{anime_data[KEY_MEDIA_ID]}'
    
    embed = Embed(
        build_media_name(anime_data),
        build_media_description(anime_data),
        url = url,
    ).add_thumbnail(
        image_url,
    )
    
    build_anime_stat_fields(embed, anime_data)
    
    return embed


def anime_response_builder_no_components(data, extra):
    embed = anime_response_builder(data, extra)
    return InteractionResponse(embed=embed, components=None)

def manga_response_builder(data, extra):
    if data is None:
        return Embed(description='No result.')
    
    manga_data = data['data'][KEY_MEDIA]
    
    image_url = manga_data[KEY_MEDIA_IMAGE][KEY_MEDIA_IMAGE_LARGE]
    url = f'{URL_BASE_MANGA}{manga_data[KEY_MEDIA_ID]}'
    
    embed = Embed(
        build_media_name(manga_data),
        build_media_description(manga_data),
        url = url,
    ).add_thumbnail(
        image_url,
    )
    
    build_manga_stat_fields(embed, manga_data)
    
    return embed


def manga_response_builder_no_components(data, extra):
    embed = manga_response_builder(data, extra)
    return InteractionResponse(embed=embed, components=None)


def array_response_builder_character(data, extra):
    return array_response_builder(data, extra, ARRAY_WORK_SET_CHARACTER)


def array_response_builder_anime(data, extra):
    return array_response_builder(data, extra, ARRAY_WORK_SET_ANIME)


def array_response_builder_manga(data, extra):
    return array_response_builder(data, extra, ARRAY_WORK_SET_MANGA)


def get_name_and_page_from_embed(embed):
    if embed is None:
        return
    
    embed_title = embed.title
    if embed_title is None:
        return
    
    embed_footer = embed.footer
    if embed_footer is None:
        return
    
    embed_footer_text = embed_footer.text
    if embed_footer_text is None:
        return
    
    matched = DECIMAL_RP.match(embed_footer_text, len('Page: '))
    if matched is None:
        return
    
    page_identifier = int(matched.group(0))
    name = embed_title[len('Search result for: '):]
    
    return name, page_identifier



@SLASH_CLIENT.interactions(
    custom_id = (
        CUSTOM_ID_FIND_CHARACTER_LEFT_DISABLED,
        CUSTOM_ID_FIND_CHARACTER_RIGHT_DISABLED,
        CUSTOM_ID_FIND_CHARACTER_SELECT_DISABLED,
        CUSTOM_ID_FIND_ANIME_LEFT_DISABLED,
        CUSTOM_ID_FIND_ANIME_RIGHT_DISABLED,
        CUSTOM_ID_FIND_ANIME_SELECT_DISABLED,
        CUSTOM_ID_FIND_MANGA_LEFT_DISABLED,
        CUSTOM_ID_FIND_MANGA_RIGHT_DISABLED,
        CUSTOM_ID_FIND_MANGA_SELECT_DISABLED,
    ),
)
async def handle_disabled_component_interaction():
    pass


@SLASH_CLIENT.interactions(is_global=True)
async def character(client, event,
        name_or_id: ('str', 'The character\'s name or it\'s id.')
            ):
    name_or_id = validate_parameter(name_or_id)
    
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_CHARACTER_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_CHARACTER,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_QUERY: name_or_id,
            },
        }
    
    return search(
        client,
        json_query,
        character_response_builder,
        None,
    )


@SLASH_CLIENT.interactions(is_global=True)
async def find_character(client, event,
        name: ('str', 'The character\'s name to try to find.')
            ):
    name = validate_parameter(name)
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        array_response_builder_character,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_CHARACTER_LEFT)
async def find_character_page_left(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        array_response_builder_character,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_CHARACTER_RIGHT)
async def find_character_page_right(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        array_response_builder_character,
        name,
    )



@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_CHARACTER_SELECT)
async def find_character_select(client, event):
    interaction = event.interaction
    if event.message.interaction.user is not event.user:
        return
    
    options = interaction.options
    if options is None:
        return
    
    option = options[0]
    try:
        character_id = int(option)
    except ValueError:
        return
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: character_id,
            },
        },
        character_response_builder_no_components,
        None,
    )



@SLASH_CLIENT.interactions(is_global=True)
async def anime_(client, event,
        name_or_id: ('str', 'The anime\'s name or it\'s id.')
            ):
    name_or_id = validate_parameter(name_or_id)
    
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_ANIME_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_ANIME,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_QUERY: name_or_id,
            },
        }
    
    return search(
        client,
        json_query,
        anime_response_builder,
        None,
    )


@SLASH_CLIENT.interactions(is_global=True)
async def find_anime(client, event,
        name: ('str', 'The anime\'s name to try to find.')
            ):
    name = validate_parameter(name)
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_anime,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_ANIME_LEFT)
async def find_anime_page_left(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_anime,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_ANIME_RIGHT)
async def find_anime_page_right(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_anime,
        name,
    )



@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_ANIME_SELECT)
async def find_anime_select(client, event):
    interaction = event.interaction
    if event.message.interaction.user is not event.user:
        return
    
    options = interaction.options
    if options is None:
        return
    
    option = options[0]
    try:
        anime_id = int(option)
    except ValueError:
        return
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: anime_id,
            },
        },
        anime_response_builder_no_components,
        None,
    )


@SLASH_CLIENT.interactions(is_global=True)
async def manga_(client, event,
        name_or_id: ('str', 'The manga\'s name or it\'s id.')
            ):
    name_or_id = validate_parameter(name_or_id)
    
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_MANGA_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_MANGA,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_QUERY: name_or_id,
            },
        }
    
    return search(
        client,
        json_query,
        manga_response_builder,
        None,
    )


@SLASH_CLIENT.interactions(is_global=True)
async def find_manga(client, event,
        name: ('str', 'The manga\'s name to try to find.')
            ):
    name = validate_parameter(name)
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_manga,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_MANGA_LEFT)
async def find_manga_page_left(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_manga,
        name,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_MANGA_RIGHT)
async def find_manga_page_right(client, event):
    message = event.message
    if message.interaction.user is not event.user:
        return
    
    name_and_page = get_name_and_page_from_embed(message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
        array_response_builder_manga,
        name,
    )



@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_FIND_MANGA_SELECT)
async def find_manga_select(client, event):
    interaction = event.interaction
    if event.message.interaction.user is not event.user:
        return
    
    options = interaction.options
    if options is None:
        return
    
    option = options[0]
    try:
        manga_id = int(option)
    except ValueError:
        return
    
    return search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: manga_id,
            },
        },
        manga_response_builder_no_components,
        None,
    )
