from re import compile as re_compile, U as re_unicode, M as re_multi_line, S as re_dotall
from hata import Client, to_json, Embed, istr, KOKORO, sleep, ScarletLock, BUILTIN_EMOJIS
from hata.backend.headers import CONTENT_TYPE
from hata.ext.slash import abort, Row, Button, InteractionResponse, Select, Option

from bot_utils.shared import GUILD__NEKO_DUNGEON

SLASH_CLIENT: Client

RATE_LIMIT_RESET_AFTER = 60.0
RATE_LIMIT_SIZE = 90

RATE_LIMIT_LOCK = ScarletLock(KOKORO, RATE_LIMIT_SIZE)

RETRY_AFTER = istr('Retry-After')

CUSTOM_ID_FIND_CHARACTER_LEFT = 'anilist.find_character.l'
CUSTOM_ID_FIND_CHARACTER_RIGHT = 'anilist.find_character.r'
CUSTOM_ID_FIND_CHARACTER_SELECT = 'anilist.find_character.s'
CUSTOM_ID_FIND_CHARACTER_EMPTY_0 = 'anilist.find_character._.0'
CUSTOM_ID_FIND_CHARACTER_EMPTY_1 = 'anilist.find_character._.1'
CUSTOM_ID_FIND_CHARACTER_EMPTY_2 = 'anilist.find_character._.2'

CHARACTER_PER_PAGE = 25
CHARACTER_URL_BASE = 'https://anilist.co/character/'

SELECT_FIND_CHARACTER_NO_RESULT = Select(
    [Option('_', 'No result', default=True)],
    CUSTOM_ID_FIND_CHARACTER_EMPTY_2,
    placeholder = 'No result',
)


EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']

DECIMAL_RP = re_compile('\d+')

KEY_CHARACTER = 'Character'
KEY_CHARACTER_ARRAY = 'characters'
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
    f'{KEY_CHARACTER_AGE}'
    # f'{KEY_CHARACTER_SITE_URL}'
    # f'{KEY_CHARACTER_FAVOURITES}'
)


CHARACTER_QUERY = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_QUERY}:String){{'
        f'{KEY_CHARACTER} ({KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)

CHARACTER_QUERY_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_ID}:Int){{'
        f'{KEY_CHARACTER} ({KEY_CHARACTER_ID}: ${KEY_VARIABLE_CHARACTER_ID}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)

CHARACTER_ARRAY_QUERY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_PER_PAGE}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:${KEY_VARIABLE_PER_PAGE}){{'
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


def validate_parameter(parameter):
    if len(parameter) > 200:
        parameter = parameter[:200]
    
    return parameter


def build_character_description(character_data):
    description = character_data[KEY_CHARACTER_DESCRIPTION]
    gender = character_data[KEY_CHARACTER_GENDER]
    blood_type = character_data[KEY_CHARACTER_BLOOD_TYPE]
    age = character_data[KEY_CHARACTER_AGE]
    
    birth_date_data = character_data[KEY_CHARACTER_BIRTH_DATE]
    
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
        description = description[:4000]+'...'
    
    return description


def build_character_array_description_and_select_row(character_array):
    character_array_length = len(character_array)
    if character_array_length:
        description_parts = []
        options = []
        
        character_array_index = 0
        
        while True:
            character_data = character_array[character_array_index]
            character_array_index += 1
            
            character_name = build_character_name(character_data)
            character_id = character_data[KEY_CHARACTER_ID]
            character_id_str = str(character_id)
            
            description_parts.append('`')
            description_parts.append(character_id_str)
            description_parts.append('`: [')
            description_parts.append(character_name)
            description_parts.append('](')
            description_parts.append(CHARACTER_URL_BASE)
            description_parts.append(character_id_str)
            description_parts.append(')')
            
            options.append(Option(character_id_str, character_name))
            if character_array_index == character_array_length:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
        select_row = Row(
            Select(
                options,
                CUSTOM_ID_FIND_CHARACTER_SELECT,
                placeholder = 'Select a character!'
            ),
        )
    
    else:
        description = 'No result.'
        select_row = SELECT_FIND_CHARACTER_NO_RESULT
    
    return description, select_row


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
    url = f'{CHARACTER_URL_BASE}{character_data[KEY_CHARACTER_ID]}'
    
    return Embed(
        build_character_name(character_data),
        build_character_description(character_data),
        url = url,
    ).add_thumbnail(
        image_url,
    )

def character_response_builder_no_components(data, extra):
    embed = character_response_builder(data, extra)
    return InteractionResponse(embed=embed, components=None)


def character_array_response_builder(data, extra):
    page_data = data['data'][KEY_PAGE]
    character_array = page_data[KEY_CHARACTER_ARRAY]
    page_info = page_data[KEY_PAGE_INFO]
    
    description, select_row = build_character_array_description_and_select_row(character_array)
    embed = Embed(
        f'Search result for: {extra}',
        description,
    )
    
    total_entries = page_info[KEY_PAGE_INFO_TOTAL_ENTRIES]
    current_page_identifier = page_info[KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER]
    total_pages = page_info[KEY_PAGE_INFO_TOTAL_PAGES]
    
    embed.add_footer(f'Page: {current_page_identifier} / {total_pages} | Total entries: {total_entries}')
    
    if current_page_identifier <= 1:
        button_left = Button(
            emoji = EMOJI_LEFT,
            custom_id = CUSTOM_ID_FIND_CHARACTER_EMPTY_0,
            enabled = False,
        )
    else:
        button_left = Button(
            emoji = EMOJI_LEFT,
            custom_id = CUSTOM_ID_FIND_CHARACTER_LEFT,
        )
    
    if current_page_identifier >= total_pages:
        button_right = Button(
            emoji = EMOJI_RIGHT,
            custom_id = CUSTOM_ID_FIND_CHARACTER_EMPTY_1,
            enabled = False,
        )
    else:
        button_right = Button(
            emoji = EMOJI_RIGHT,
            custom_id = CUSTOM_ID_FIND_CHARACTER_RIGHT,
        )
    
    return InteractionResponse(
        embed = embed,
        components = [
            select_row,
            Row(button_left, button_right),
        ],
    )



@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def character(client, event,
        name_or_id: ('str', 'The character\'s name or it\'s id.')
            ):
    name_or_id = validate_parameter(name_or_id)
    
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: CHARACTER_QUERY_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: CHARACTER_QUERY,
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


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def find_character(client, event,
        name: ('str', 'The character\'s name to try to find.')
            ):
    name = validate_parameter(name)
    
    return search(
        client,
        {
            KEY_QUERY: CHARACTER_ARRAY_QUERY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_PER_PAGE: CHARACTER_PER_PAGE,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        character_array_response_builder,
        name,
    )

 
@SLASH_CLIENT.interactions(
    custom_id = (
            CUSTOM_ID_FIND_CHARACTER_EMPTY_0,
            CUSTOM_ID_FIND_CHARACTER_EMPTY_1,
            CUSTOM_ID_FIND_CHARACTER_EMPTY_2,
    ),
)
async def handle_disabled_component_interaction():
    pass


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
            KEY_QUERY: CHARACTER_ARRAY_QUERY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_PER_PAGE: CHARACTER_PER_PAGE,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        character_array_response_builder,
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
            KEY_QUERY: CHARACTER_ARRAY_QUERY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_PER_PAGE: CHARACTER_PER_PAGE,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
        character_array_response_builder,
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
            KEY_QUERY: CHARACTER_QUERY_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: character_id,
            },
        },
        character_response_builder_no_components,
        None,
    )
