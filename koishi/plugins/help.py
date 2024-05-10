__all__ = ()

from functools import partial as partial_func
from time import perf_counter

from hata import BUILTIN_EMOJIS, Embed, Emoji
from hata.ext.slash import Button, InteractionResponse, Row, abort
from hata.ext.slash.menus import Closer, Pagination

from ..bot_utils.constants import (
    COLOR__KOISHI_HELP, EMOJI__HEART_CURRENCY, GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT, URL__KOISHI_TOP_GG,
    ROLE__SUPPORT__ANNOUNCEMENTS, ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__EVENT_MANAGER,
    ROLE__SUPPORT__EVENT_PARTICIPANT, ROLE__SUPPORT__EVENT_WINNER, ROLE__SUPPORT__HEART_BOOST,
    ROLE__SUPPORT__NSFW_ACCESS, ROLE__SUPPORT__VERIFIED
)
from ..bot_utils.headers import get_header_for
from ..bots import FEATURE_CLIENTS


HATA_DOCS_BASE_URL = 'https://www.astil.dev/project/hata/docs/'
HATA_DOCS_SEARCH_API = HATA_DOCS_BASE_URL + 'api/v1/search'

CLAIM_ROLE_VERIFIED_EMOJI = Emoji.precreate(931503291957919744)
CLAIM_ROLE_VERIFIED_CUSTOM_ID = 'rules.claim_role.verified'

CLAIM_ROLE_ANNOUNCEMENTS_EMOJI = Emoji.precreate(1175518140390707332)
CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID = 'rules.claim_role.announcements'

RULES_COMPONENTS = Row(
    Button(
        'Accept rules (I wont fry fumos)',
        CLAIM_ROLE_VERIFIED_EMOJI,
        custom_id = CLAIM_ROLE_VERIFIED_CUSTOM_ID,
    ),
    Button(
        'Claim announcements role',
        CLAIM_ROLE_ANNOUNCEMENTS_EMOJI,
        custom_id = CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID,
    ),
)


RULES = [
    (
        'Behaviour',
        lambda: 'Listen to staff and follow their instructions.',
    ), (
        'Language',
        lambda: f'{GUILD__SUPPORT.name} is an english speaking server, please try to stick yourself to it.'
    ), (
        'Channels',
        lambda: 'Read the channel\'s topics. Make sure to keep the conversations in their respective channels.'
    ), (
        'Usernames',
        lambda: 'Invisible, offensive or noise unicode names are not allowed.',
    ), (
        'Spamming',
        lambda: 'Forbidden in any form. Spamming server members in DM-s counts as well.'
    ), (
        'NSFW',
        lambda: 'Keep explicit content in nsfw channels.',
    ), (
        'Shitposting, earrape and other cursed contents',
        lambda: (
            'Including tiktok cringe, ai shit, pictures taken of a screen, '
            'and making the same joke 3 times in a row are all a big NO!!!'
        ),
    ), (
        'Advertisements',
        lambda: 'Advertising other social medias, servers, communities or services in chat or in DM-s are disallowed.',
    ), (
        'Political and Religious topics',
        lambda: 'I do not say either that aliens exists, even tho they do.',
    ), (
        'Alternative accounts',
        lambda: 'Unless, you have really good reason, like you were locked out from the original.',
    ), (
        'Deep frying fumos',
        lambda: 'Fumo frying and other related unethical actions are bannable offenses.',
    )
]

#     (
#         'Chat identity',
#         lambda: f'{GUILD__SUPPORT.name} is a Touhou themed guild so everyone is identified as a Touhou girl.',
#     ),


RULE_CHOICES = [(f'{index}. {title}', index) for index, (title, description_builder) in enumerate(RULES)]


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    description = f'{GUILD__SUPPORT.name}\'s rules!'
)
async def rules(
    event,
    rule: (RULE_CHOICES, 'Select a rule to show.') = None
):
    if rule is None:
        description_parts = []
        for index, (title, description_builder) in enumerate(RULES):
            description_parts.append(f'**{index}\\. {title}**\n')
            description_parts.append(description_builder())
            description_parts.append('\n\n')
        
        description_parts.append(
            'If ever in doubt about rules, follow [Discord\'s guidelines](https://discord.com/guidelines).'
        )
        
        description = ''.join(description_parts)
        description_parts = None
        
        embed = Embed(
            f'Rules of {GUILD__SUPPORT.name}:',
            description,
            color = COLOR__KOISHI_HELP,
        )
        
        if event.user_permissions.can_administrator:
            components = RULES_COMPONENTS
        else:
            components = None

    else:
        embed = Embed(
            f'Rules {rule} of {GUILD__SUPPORT.name}:',
            color = COLOR__KOISHI_HELP,
        )
        
        title, description_builder = RULES[rule]
        embed.add_field(title, description_builder())
        components = None
    
    return InteractionResponse(embed = embed, components = components, allowed_mentions = None)


@FEATURE_CLIENTS.interactions(custom_id = CLAIM_ROLE_VERIFIED_CUSTOM_ID)
async def claim_verified_role(client, event):
    """
    Assigns the verified role to the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    user = event.user
    if user.has_role(ROLE__SUPPORT__VERIFIED):
        response = f'You already have {ROLE__SUPPORT__VERIFIED.name} role claimed.'
    else:
        await client.user_role_add(user, ROLE__SUPPORT__VERIFIED)
        response = f'You claimed {ROLE__SUPPORT__VERIFIED.name} role.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)


@FEATURE_CLIENTS.interactions(custom_id = CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID, show_for_invoking_user_only = True)
async def claim_announcements_role(client, event):
    """
    Assigns or removes the announcements role to / of the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    user = event.user
    if user.has_role(ROLE__SUPPORT__ANNOUNCEMENTS):
        await client.user_role_delete(user, ROLE__SUPPORT__ANNOUNCEMENTS)
        response = f'Your {ROLE__SUPPORT__ANNOUNCEMENTS.name} role was removed.'
    else:
        await client.user_role_add(user, ROLE__SUPPORT__ANNOUNCEMENTS)
        response = f'You claimed {ROLE__SUPPORT__ANNOUNCEMENTS.name} role.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)



def docs_search_pagination_check(user, event):
    if user is event.user:
        return True
    
    if event.user_permissions.can_manage_messages:
        return True
    
    return False


EMOJI_TOOLS = BUILTIN_EMOJIS['tools']
EMOJI_RING = BUILTIN_EMOJIS['ring']
EMOJI_SPEECH_BUBBLE = BUILTIN_EMOJIS['speech_balloon']
EMOJI_VIDEO_GAME = BUILTIN_EMOJIS['video_game']
EMOJI_WAIFU = BUILTIN_EMOJIS['woman_with_veil']
EMOJI_PAPER_DRAGON = BUILTIN_EMOJIS['kite']
EMOJI_MAGIC_WAND = BUILTIN_EMOJIS['magic_wand']
EMOJI_PILL = BUILTIN_EMOJIS['pill']
EMOJI_MASKS = BUILTIN_EMOJIS['performing_arts']

CATEGORIES = (
    (
        'Administration',
        EMOJI_TOOLS,
        ('automation', 'clear', 'dupe-image-filter', 'invite-create', 'mod', 'self-mod'),
        (
            'all-users', 'automation', 'copy-message', 'in-role','latest-users', 'move-message', 'move-channel',
            'move-messages'
        ),
    ), (
        'Anime',
        EMOJI_PILL,
        ('anime', 'character', 'find-anime', 'find-character', 'find-manga', 'manga',),
        (),
    ), (
        'Actions',
        EMOJI_MASKS,
        (
            'bite', 'blush', 'bully', 'cringe', 'cry', 'dance', 'feed', 'fluff', 'glomp', 'handhold', 'happy',
            'highfive', 'hug', 'kick', 'kill', 'kiss', 'kon', 'lick', 'like', 'nom', 'pat', 'pocky-kiss', 'poke',
            'slap', 'smile', 'smug', 'wave', 'wink', 'yeet',
        ),
        (),
    ), (
        'Economy',
        EMOJI__HEART_CURRENCY,
        ('daily', 'gift', 'heart-shop', 'hearts', 'top-list',),
        (),
    ), (
        'Fun',
        EMOJI_PAPER_DRAGON,
        (
            '9ball', 'ascii', 'meme', 'message-me', 'minesweeper', 'oj', 'paranoia', 'random', 'rate', 'roll',
            'sex', 'stats', 'trivia', 'urban', 'yuno'
        ),
        (),
    ), (
        'Games',
        EMOJI_VIDEO_GAME,
        ('21', 'ds', 'kanako', 'lucky-spin', 'xox',),
        (),
    ), (
        'Help',
        EMOJI_SPEECH_BUBBLE,
        ('about', 'help',),
        (),
    ), (
        'Marriage',
        EMOJI_RING,
        ('divorce', 'love', 'propose', 'proposals', 'waifu-info',),
        (),
    ), (
        'Utility',
        EMOJI_MAGIC_WAND,
        (
            'calc', 'choose', 'create-activity', 'color', 'format-time', 'guild', 'id',
            'ping', 'rawr', 'role-info', 'roles', 'snipe', 'style-text', 'user'
        ),
        (),
    ), (
        'Waifus',
        EMOJI_WAIFU,
        (
            'nsfwbooru', 'safebooru', 'touhou-calendar', 'touhou-character', 'vocaloid', 'waifu-safe',
            'waifu-nsfw'
        ),
        (),
    ),
)


NOT_LISTED_COMMANDS = ('koi-guilds', 'koi-guilds-how-to')

"""
def build_category_into(extend, category_name, emoji, command_names):
    extend.append(emoji.as_emoji)
    extend.append(' **')
    extend.append(category_name)
    extend.append('**\n')
    
    length = len(command_names)
    if length:
        index = 0
        while True:
            command_name = command_names[index]
            index += 1
            
            extend.append('`')
            extend.append(command_name)
            extend.append('`')
            
            if index == length:
                break
            
            extend.append(' **•** ')
            continue
    else:
        extend.append('*none*')
    
    return extend


def build_command_list_embed(header, extended):
    length = len(CATEGORIES)
    
    description_parts = []
    description_parts.append(header)
    
    if length:
        description_parts.append('\n')
        
        index = 0
        
        while True:
            category = CATEGORIES[index]
            index += 1
            
            commands = category[2]
            if extended:
                commands = sorted(commands + category[3])
            
            build_category_into(description_parts, category[0], category[1], commands)
            
            if index == length:
                break
            
            description_parts.append('\n\n')
            continue
        
    description = ''.join(description_parts)
    
    return Embed(
        description,
        color = COLOR__KOISHI_HELP,
    )
"""

def build_command_list_embed(header, extended):
    embed = Embed(
        None,
        header,
        color = COLOR__KOISHI_HELP,
    )
    
    for (name, emoji, command_names, extra) in CATEGORIES:
        if extended:
            command_names = sorted(command_names + extra)
        
        embed.add_field(
            f'{name} {emoji}',
            ' **•** '.join([f'`{command_name}`' for command_name in command_names]),
        )
    
    return embed


HEARD_GUIDE_EMBED = Embed(
    'Heart Guide',
    color = COLOR__KOISHI_HELP,
).add_thumbnail(
    EMOJI__HEART_CURRENCY.url,
).add_field(
    'Getting hearts',
    (
        f'**•** `/daily` - Claim you daily reward.\n'
        f'**•** `/ds` - Complete dungeon sweeper stages.\n'
        f'**•** `/proposal accept` - Accept marriage proposals.\n'
        f'**•** `/heart-shop sell-daily` - Sell your daily streak.\n'
        f'**•** [Vote]({URL__KOISHI_TOP_GG}) on me on top.gg\n'
        f'**•** Use any command to get hearts randomly.'
    ),
).add_field(
    'Spending hearts',
    (
        '**•** `/propose` - Propose to your heart\'s chosen one.\n'
        '**•** `/divorce` - Less waifus.\n'
        '**•** `/heart-shop roles` - Buy roles inside of my support server.\n'
        '**•** `/heart-shop waifu-slot` - More waifus.\n'
        '**•** `/stats upgrade` - Upgrade your waifus stats.'
    ),
).add_field(
    'Gambling hearts',
    (
        '**•** `/21` - Almost Blackjack.\n'
        '**•** `/lucky-spin` - Lucky spin.'
    ),
)

async def render_help_generic(client, event):
    return build_command_list_embed(get_header_for(client), event.guild is GUILD__ORIN_PARTY_HOUSE)


async def render_help_heart_guide(client, event):
    return HEARD_GUIDE_EMBED


CUSTOM_ID_HELP_CLOSE = 'help.close'


HELP_COMPONENTS = Row(
    Button(
        'Close',
        BUILTIN_EMOJIS['x'],
        custom_id = CUSTOM_ID_HELP_CLOSE,
    )
)


HELP_FIELD_NAME_GENERIC = 'generic'
HELP_FIELD_NAME_HEART_GUIDE = 'heart-guide'

HELP_FIELD_CHOICES = [
    HELP_FIELD_NAME_GENERIC,
    HELP_FIELD_NAME_HEART_GUIDE,
]

HELP_FIELD_NAME_TO_RENDERER = {
    HELP_FIELD_NAME_GENERIC: render_help_generic,
    HELP_FIELD_NAME_HEART_GUIDE: render_help_heart_guide,
}

@FEATURE_CLIENTS.interactions(is_global = True)
async def help_(
    client,
    event,
    field: (HELP_FIELD_CHOICES, 'Choose a field!') = HELP_FIELD_NAME_GENERIC,
):
    """
    Lists my commands and such.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    field : `str` == `'generic'`, Optional
        Which field to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    try:
        field_renderer = HELP_FIELD_NAME_TO_RENDERER[field]
    except KeyError:
        return abort(f'Unknown field: {field!r}.')
    
    embed = await field_renderer(client, event)
    return InteractionResponse(
        embed = embed,
        components = HELP_COMPONENTS,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_HELP_CLOSE)
async def help_close(client, event):
    """
    Closes the help message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    if event.user_permissions.can_manage_messages or event.message.interaction.user_id == event.user_id:
        await client.interaction_response_message_delete(event)
    
    else:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )


@FEATURE_CLIENTS.interactions(is_global = True, wait_for_acknowledgement = True)
async def ping(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter() - start) * 1000.0
    
    yield Embed(
        'Ping',
    ).add_field(
        'Acknowledge latency',
        (
            f'```\n'
            f'{delay:.0f} ms\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Gateway latency',
        (
            f'```\n'
            f'{client.gateway.latency * 1000.:.0f} ms\n'
            f'```'
        ),
        inline = True,
    )


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def docs_search(client, event,
    search_for: ('str', 'Search term'),
):
    """Searchers the given query from hata docs."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command', color = COLOR__KOISHI_HELP)
        return
    
    if (client.get_guild_profile_for(guild) is None):
        yield Embed('Error', 'I must be in the guild to execute this command.', color = COLOR__KOISHI_HELP)
        return
    
    if len(search_for) < 4:
        yield Embed('Ohoho', 'Please give a longer query', color = COLOR__KOISHI_HELP)
        return
    
    yield
    
    async with client.http.get(HATA_DOCS_SEARCH_API, params={'search_for': search_for}) as response:
        datas = await response.json()
    
    if not datas:
        embed = Embed(f'No search result for: `{search_for}`', color = COLOR__KOISHI_HELP)
        await Closer(client, event, embed)
        return
    
    sections = []
    section_parts = []
    for data in datas:
        section_parts.append('[**')
        name = data['name']
        name = name.replace('_', '\_')
        section_parts.append(name)
        section_parts.append('**](')
        section_parts.append(HATA_DOCS_BASE_URL)
        url = data['url']
        section_parts.append(url)
        section_parts.append(') *')
        type_ = data['type']
        section_parts.append(type_)
        section_parts.append('*')
        preview = data.get('preview', None)
        if (preview is not None):
            preview = preview.replace('_', '\_')
            section_parts.append('\n')
            section_parts.append(preview)
        
        section = ''.join(section_parts)
        sections.append(section)
        section_parts.clear()
    
    
    descriptions = []
    description_parts = []
    description_length = 0
    
    for section in sections:
        section_length = len(section)
        description_length += section_length
        if description_length > 2000:
            description = ''.join(description_parts)
            descriptions.append(description)
            description_parts.clear()
            
            description_parts.append(section)
            description_length = section_length
            continue
        
        if description_parts:
            description_parts.append('\n\n')
            description_length += 2
        
        description_parts.append(section)
        continue
    
    if description_parts:
        description = ''.join(description_parts)
        descriptions.append(description)
    
    
    title = f'Search results for `{search_for}`'
    
    embeds = []
    for index, description in enumerate(descriptions, 1):
        embed = Embed(title, description, color = COLOR__KOISHI_HELP).add_footer(f'Page {index}/{len(descriptions)}')
        embeds.append(embed)
    
    await Pagination(client, event, embeds, check = partial_func(docs_search_pagination_check, event.user))


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def ask():
    """How to ask!"""
    return Embed(
        'How to ask?',
        (
            'Don\'t ask to ask just ask.\n'
            '\n'
            ' • You will have much higher chances of getting an answer\n'
            ' • It saves time both for us and you as we can skip the whole process of actually getting the question '
            'out of you\n'
            '\n'
            'For more info visit [dontasktoask.com](https://dontasktoask.com/)'
        ),
        color = COLOR__KOISHI_HELP,
    )


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def markdown():
    """How to use markdown."""
    return Embed(
        'Markdown',
        (
            'You can format your code by using markdown like this:\n'
            '\n'
            '\\`\\`\\`py\n'
            'print(\'Hello world\')\n'
            '\\`\\`\\`\n'
            '\n'
            'This would give you:\n'
            '```python\n'
            'print(\'Hello world\')```\n'
            'Note that character \` is not a quote but a backtick.\n'
            '\n'
            f'If, however, you have large amounts of code then upload it as a file.'
        ),
        color = COLOR__KOISHI_HELP,
    )



ROLE_INFO = FEATURE_CLIENTS.interactions(
    None,
    name = 'roles',
    description = 'Role information!',
    guild = GUILD__SUPPORT,
)


@ROLE_INFO.interactions
async def collectible():
    """A list of collectible roles in KW."""
    embed = Embed(
        'Collectible roles:',
        f'Collect roles by buying them for heart {EMOJI__HEART_CURRENCY} using the `heart-shop roles` command.',
        color = COLOR__KOISHI_HELP,
    ).add_field(
        ROLE__SUPPORT__NSFW_ACCESS.name,
        f'Gives access to nsfw channels.',
    ).add_field(
        ROLE__SUPPORT__ELEVATED.name,
        f'Unlocks secret nekogirl only content.',
    ).add_field(
        ROLE__SUPPORT__HEART_BOOST.name,
        f'Become favored by Koishi receiving more hearts from her each day.',
    )
    
    return InteractionResponse(embed = embed, allowed_mentions = None)


@ROLE_INFO.interactions
async def events():
    """Event related role information."""
    embed = Embed(
        'Event roles',
        color = COLOR__KOISHI_HELP,
    ).add_field(
        ROLE__SUPPORT__EVENT_PARTICIPANT.name,
        f'{ROLE__SUPPORT__EVENT_PARTICIPANT.mention} are participant of the actual event.'
    ).add_field(
        ROLE__SUPPORT__EVENT_WINNER.name,
        f'{ROLE__SUPPORT__EVENT_WINNER.mention} won already an event. It is set in stone, only a couple of '
        f'chads may achieve this level of power.'
    ).add_field(
        ROLE__SUPPORT__EVENT_MANAGER.name,
        f'{ROLE__SUPPORT__EVENT_MANAGER.mention} are managing the actual event. Hoping our god ZUN will '
        f'notice them one day.'
    )
    
    return InteractionResponse(embed = embed, allowed_mentions = None)
