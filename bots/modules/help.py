import sys
from functools import partial as partial_func

from hata import CLIENTS, USERS, GUILDS, Embed, Client, __version__, Emoji
from hata.ext.slash.menus import Pagination, Closer
from hata.ext.slash import InteractionResponse, Button, Row

from bot_utils.shared import LINK__KOISHI_GIT, LINK__HATA_GIT, INVITE__NEKO_DUNGEON, GUILD__NEKO_DUNGEON, \
    LINK__HATA_DOCS, LINK__PASTE, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, COLOR__KOISHI_HELP, ROLE__NEKO_DUNGEON__ELEVATED, \
    ROLE__NEKO_DUNGEON__VERIFIED, CHANNEL__NEKO_DUNGEON__SYSTEM, LINK__HATA_SLASH, ROLE__NEKO_DUNGEON__NSFW_ACCESS, \
    ROLE__NEKO_DUNGEON__EVENT_MANAGER, ROLE__NEKO_DUNGEON__EVENT_WINNER, ROLE__NEKO_DUNGEON__EVENT_PARTICIPANT, \
    EMOJI__HEART_CURRENCY, ROLE__NEKO_DUNGEON__HEART_BOOST


SLASH_CLIENT: Client

HATA_DOCS_BASE_URL = 'https://www.astil.dev/project/hata/docs/'
HATA_DOCS_SEARCH_API = HATA_DOCS_BASE_URL + 'api/v1/search'

CLAIM_ROLE_VERIFIED_EMOJI = Emoji.precreate(690550890045898812)
CLAIM_ROLE_VERIFIED_CUSTOM_ID = 'rules.claim_role.verified'

CLAIM_ROLE_ANNOUNCEMENTS_EMOJi = Emoji.precreate(717841004383961221)
CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID = 'rules.claim_role.announcements'

RULES_COMPONENTS = Row(
    Button(
        'Accept rules (I wont fry fumos)',
        CLAIM_ROLE_VERIFIED_EMOJI,
        custom_id = CLAIM_ROLE_VERIFIED_CUSTOM_ID,
    ),
    Button(
        'Claim announcements role',
        CLAIM_ROLE_ANNOUNCEMENTS_EMOJi,
        custom_id = CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID,
    ),
)

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def rules(client, event):
    """Neko Dungeon\'s rules!"""
    embed = Embed(f'Rules of {GUILD__NEKO_DUNGEON}:', color=COLOR__KOISHI_HELP,
        ).add_field(
            '0. Guidelines',
            'Follow [Discord\'s guidelines](https://discord.com/guidelines)',
        ).add_field(
            '1. Behaviour',
            'Listen to staff and follow their instructions.',
        ).add_field(
            '2. Language',
            f'{GUILD__NEKO_DUNGEON} is an english speaking server, please try to stick yourself to it.',
        ).add_field(
            '3. Channels',
            'Read the channel\'s topics. Make sure to keep the conversations in their respective channels.'
        ).add_field(
            '4. Usernames',
            'Invisible, offensive or noise unicode names are not allowed.'
        ).add_field(
            '5. Spamming',
            'Forbidden in any form. Spamming server members in DM-s counts as well.',
        ).add_field(
            '6. NSFW',
            'Keep explicit content in nsfw channels.',
        ).add_field(
            '7. Advertisements',
            'Advertising other social medias, servers, communities or services in chat or in DM-s are disallowed.'
        ).add_field(
            '8. No political or religious topics.',
            'I do not say either that aliens exists, even tho they do.',
        ).add_field(
            '9. Alternative accounts',
            'Instant ban.'
        ).add_field(
            '10. Deep frying fumos',
            'Fumo frying is bannable offense.'
        )
    
    if client.is_owner(event.user):
        components = RULES_COMPONENTS
    else:
        components = None
    
    return InteractionResponse(embed=embed, components=components, allowed_mentions=None)


@SLASH_CLIENT.interactions(custom_id=CLAIM_ROLE_VERIFIED_CUSTOM_ID)
async def claim_verified_role(client, event):
    user = event.user
    if not user.has_role(ROLE__NEKO_DUNGEON__VERIFIED):
        await client.user_role_add(user, ROLE__NEKO_DUNGEON__VERIFIED)


@SLASH_CLIENT.interactions(custom_id=CLAIM_ROLE_ANNOUNCEMENTS_CUSTOM_ID)
async def claim_announcements_role(client, event):
    user = event.user
    if user.has_role(ROLE__NEKO_DUNGEON__ANNOUNCEMENTS):
        await client.user_role_delete(user, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS)
    else:
        await client.user_role_add(user, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS)


def create_interpreter_info():
    implementation = sys.implementation
    version = implementation.version
    main_version_number = version[0]
    sub_version_number = version[1]
    release = version[3]
    
    interpreter_info_parts = []
    
    interpreter_info_parts.append('Python')
    interpreter_info_parts.append(repr(main_version_number))
    interpreter_info_parts.append('.')
    interpreter_info_parts.append(repr(sub_version_number))
    
    if release != 'final':
        interpreter_info_parts.append(' ')
        interpreter_info_parts.append(release)
    
    interpreter_info_parts.append(' ')
    interpreter_info_parts.append(implementation.name)
    
    return ''.join(interpreter_info_parts)

INTERPRETER_INFO = create_interpreter_info()

def create_library_info():
    return (
        f'[hata {__version__}]({LINK__HATA_GIT})\n'
        f'[Slash commands]({LINK__HATA_SLASH})\n'
        f'[Technical documentation]({LINK__HATA_DOCS})'
    )

LIBRARY_INFO = create_library_info()

@SLASH_CLIENT.interactions(is_global=True)
async def about(client):
    """My loli secret. Simpers only!"""
    return Embed(
        'About',
        f'Hello, I am {client.full_name} as you expected. It was a great success to meat you!',
        color=COLOR__KOISHI_HELP,
        ).add_field(
            'Library',
            LIBRARY_INFO,
            inline = True,
        ).add_field(
            'Git',
            f'[Koishi repository]({LINK__KOISHI_GIT})',
            inline = True,
        ).add_field(
            'Support server',
            f'[{GUILD__NEKO_DUNGEON.name}]({INVITE__NEKO_DUNGEON.url})',
            inline = True,
        ).add_field('Interpreter',
            INTERPRETER_INFO,
            inline = True,
        ).add_field(
            'Client info',
            (
                f'Clients: {len(CLIENTS)}\n'
                f'Guilds: {len(GUILDS)}\n'
                f'Users: {len(USERS)}'
            ),
            inline = True,
        ).add_thumbnail(
            client.application.icon_url_as(size=128)
        )



def docs_search_pagination_check(user, event):
    if user is event.user:
        return True
    
    if event.user_permissions.can_manage_messages:
        return True
    
    return False


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def docs_search(client, event,
        search_for: ('str', 'Search term'),
            ):
    """Searchers the given query from hata docs."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command', color=COLOR__KOISHI_HELP)
        return
    
    if (client.get_guild_profile_for(guild) is None):
        yield Embed('Error', 'I must be in the guild to execute this command.', color=COLOR__KOISHI_HELP)
        return
    
    if len(search_for) < 4:
        yield Embed('Ohoho', 'Please give a longer query', color=COLOR__KOISHI_HELP)
        return
    
    yield
    
    async with client.http.get(HATA_DOCS_SEARCH_API, params={'search_for': search_for}) as response:
        datas = await response.json()
    
    if not datas:
        embed = Embed(f'No search result for: `{search_for}`', color=COLOR__KOISHI_HELP)
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
        embed = Embed(title, description, color=COLOR__KOISHI_HELP).add_footer(f'Page {index}/{len(descriptions)}')
        embeds.append(embed)
    
    await Pagination(client, event, embeds, check=partial_func(docs_search_pagination_check, event.user))


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def ask():
    """How to ask!"""
    return Embed('How to ask?',
        'Don\'t ask to ask just ask.\n'
        '\n'
        ' • You will have much higher chances of getting an answer\n'
        ' • It saves time both for us and you as we can skip the whole process of actually getting the question '
        'out of you\n'
        '\n'
        'For more info visit [dontasktoask.com](https://dontasktoask.com/)',
            color = COLOR__KOISHI_HELP)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def markdown():
    """How to use markdown."""
    return Embed('Markdown',
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
        f'If, however, you have large amounts of code then it\'s better to use [our paste service]({LINK__PASTE}).',
            color = COLOR__KOISHI_HELP)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def paste():
    """A link to our paste service."""
    return Embed(description=f'[Paste link]({LINK__PASTE})', color=COLOR__KOISHI_HELP)



ROLES = SLASH_CLIENT.interactions(None,
    name = 'roles',
    description = 'Role information!',
    guild=GUILD__NEKO_DUNGEON,
)


@ROLES.interactions
async def Collectible():
    """A list of collectible roles in ND."""
    embed = Embed('Collectible roles:',
        f'Collect roles by buying them for heart {EMOJI__HEART_CURRENCY:e} using the `heart-shop roles` command.',
        color = COLOR__KOISHI_HELP,
    ).add_field(
        ROLE__NEKO_DUNGEON__NSFW_ACCESS.name,
        f'Gives access to nsfw channels.',
    ).add_field(
        ROLE__NEKO_DUNGEON__ELEVATED.name,
        f'Unlocks secret nekogirl only content.',
    ).add_field(
        ROLE__NEKO_DUNGEON__HEART_BOOST.name,
        f'Become favored by Koishi receiving more hearts from her each day.',
    )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


@ROLES.interactions
async def events():
    """Event related role information."""
    embed = Embed(
        'Event roles',
        color = COLOR__KOISHI_HELP,
    ).add_field(
        ROLE__NEKO_DUNGEON__EVENT_PARTICIPANT.name,
        f'{ROLE__NEKO_DUNGEON__EVENT_PARTICIPANT.mention} are participant of the actual event.'
    ).add_field(
        ROLE__NEKO_DUNGEON__EVENT_WINNER.name,
        f'{ROLE__NEKO_DUNGEON__EVENT_WINNER.mention} won already an event. It is set in stone, only a couple of '
        f'chads may achieve this level of power.'
    ).add_field(
        ROLE__NEKO_DUNGEON__EVENT_MANAGER.name,
        f'{ROLE__NEKO_DUNGEON__EVENT_MANAGER.mention} are managing the actual event. Hoping our god ZUN will '
        f'notice them one day.'
    )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)
