from re import compile as re_compile, U as re_unicode, M as re_multi_line, S as re_dotall
from hata import Client, to_json, Embed, istr, KOKORO, sleep, ScarletLock
from hata.backend.headers import CONTENT_TYPE
from hata.ext.slash import abort

from bot_utils.shared import GUILD__NEKO_DUNGEON

SLASH_CLIENT: Client

RATE_LIMIT_RESET_AFTER = 60.0
RATE_LIMIT_SIZE = 90

RATE_LIMIT_LOCK = ScarletLock(KOKORO, RATE_LIMIT_SIZE)

RETRY_AFTER = istr('Retry-After')

KEY_SITE_URL = 'siteUrl'
KEY_CHARACTER = 'Character'
KEY_NAME = 'name'
KEY_NAME_FIRST = 'last'
KEY_NAME_MIDDLE = 'middle'
KEY_NAME_LAST = 'first'
KEY_NAME_NATIVE = 'native'
KEY_NAME_ALTERNATIVE = 'alternative'
KEY_NAME_ALTERNATIVE_SPOILER = 'alternativeSpoiler'
KEY_NAME_USER_PREFERRED = 'userPreferred'
KEY_NAME_FULL = 'full'
KEY_DESCRIPTION = 'description'
KEY_IMAGE = 'image'
KEY_IMAGE_LARGE = 'large'
KEY_ID = 'id'
KEY_FAVOURITES = 'favourites'
KEY_BIRTH_DATE = 'dateOfBirth'
KEY_FUZZY_DATE_YEAR = 'year'
KEY_FUZZY_DATE_MONTH = 'month'
KEY_FUZZY_DATE_DAY = 'day'
KEY_GENDER = 'gender'
KEY_BLOOD_TYPE = 'bloodType'
KEY_AGE = 'age'

KEY_QUERY = 'query'
KEY_VARIABLES = 'variables'

KEY_VARIABLE_QUERY = 'query'
KEY_VARIABLE_ID = 'id'

REQUIRED_CHARACTER_FIELDS = (
    # f'{KEY_ID}'
    f'{KEY_NAME}{{'
        f'{KEY_NAME_FIRST} '
        f'{KEY_NAME_MIDDLE} '
        f'{KEY_NAME_LAST} '
        f'{KEY_NAME_NATIVE}'
    f'}}'
    f'{KEY_IMAGE}{{'
        f'{KEY_IMAGE_LARGE}'
    f'}}'
    f'{KEY_BIRTH_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_DESCRIPTION} '
    f'{KEY_GENDER} '
    f'{KEY_BLOOD_TYPE} '
    f'{KEY_AGE} '
    f'{KEY_SITE_URL}'
    # f'{KEY_FAVOURITES}'
)

CHARACTER_QUERY = (
    f'query (${KEY_VARIABLE_QUERY}: String){{'
        f'{KEY_CHARACTER} (search: ${KEY_VARIABLE_QUERY}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)

CHARACTER_QUERY_BY_ID = (
    f'query (${KEY_VARIABLE_ID}: Int){{'
        f'{KEY_CHARACTER} ({KEY_ID}: ${KEY_VARIABLE_ID}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
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


def build_character_name(character_data):
    name_data = character_data[KEY_NAME]
    name_first = name_data[KEY_NAME_FIRST]
    name_middle = name_data[KEY_NAME_MIDDLE]
    name_last = name_data[KEY_NAME_LAST]
    name_native = name_data[KEY_NAME_NATIVE]
    
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


DESCRIPTION_RP = re_compile(
    (
        '~!|' # Spoiler tag
        '!~|' # Spoiler tag ending
        '__|' # bold
        ' \(\d+\'(?:\d+\")?\)' # US shit
    ),
    re_multi_line|re_unicode|re_dotall,
)

DESCRIPTION_RELATION = {
    '~!': '||',
    '!~': '||',
    '__': '**',
}

def DESCRIPTION_REPLACER(match):
    return DESCRIPTION_RELATION.get(match.group(0), '')


def build_character_description(character_data):
    description = character_data[KEY_DESCRIPTION]
    gender = character_data[KEY_GENDER]
    blood_type = character_data[KEY_BLOOD_TYPE]
    age = character_data[KEY_AGE]
    
    birth_date_data = character_data[KEY_BIRTH_DATE]
    
    description_parts = []
    
    birth_date_value = build_fuzzy_date(birth_date_data)
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
    
    if (description is not None):
        description = DESCRIPTION_RP.sub(DESCRIPTION_REPLACER, description)
        
        if field_added:
            if description.startswith('**'):
                description_parts.append('\n')
            else:
                description_parts.append('\n\n')
        
        description_parts.append(description)
    
    description = ''.join(description_parts)
    
    if len(description) > 4000:
        description = description[:4000]
    
    return description


async def search(client, json_query, response_builder):
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
    
    
    yield response_builder(data)


def character_response_builder(data):
    if data is None:
        return Embed(description='No result.')
    
    character_data = data['data'][KEY_CHARACTER]
    
    image_url = character_data[KEY_IMAGE][KEY_IMAGE_LARGE]
    url = character_data[KEY_SITE_URL]
    
    return Embed(
        build_character_name(character_data),
        build_character_description(character_data),
        url = url,
    ).add_thumbnail(
        image_url,
    )


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def character(client, event,
        name_or_id: ('str', 'The character\'s name or it\'s id.')
            ):
    
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: CHARACTER_QUERY_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_ID : int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: CHARACTER_QUERY,
            KEY_VARIABLES: {
                KEY_VARIABLE_QUERY: name_or_id,
            },
        }
    
    return search(
        client,
        json_query,
        character_response_builder,
    )
