import sys
from functools import partial as partial_func

from hata import CLIENTS, USERS, GUILDS, Embed, Client, __version__
from hata.ext.slash.menus import Pagination, Closer
from hata.ext.slash import InteractionResponse

from bot_utils.shared import LINK__KOISHI_GIT, LINK__HATA_GIT, INVITE__NEKO_DUNGEON, GUILD__NEKO_DUNGEON, \
    LINK__HATA_DOCS, LINK__PASTE, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, COLOR__KOISHI_HELP, ROLE__NEKO_DUNGEON__ELEVATED, \
    ROLE__NEKO_DUNGEON__VERIFIED, CHANNEL__NEKO_DUNGEON__SYSTEM, LINK__HATA_SLASH, ROLE__NEKO_DUNGEON__NSFW_ACCESS, \
    ROLE__NEKO_DUNGEON__EVENT_MANAGER, ROLE__NEKO_DUNGEON__EVENT_WINNER, ROLE__NEKO_DUNGEON__EVENT_PARTICIPANT


SLASH_CLIENT: Client

HATA_DOCS_BASE_URL = 'https://www.astil.dev/project/hata/docs/'
HATA_DOCS_SEARCH_API = HATA_DOCS_BASE_URL + 'api/v1/search'

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
            '7. Roles',
            f'Do not beg for roles. You can claim {ROLE__NEKO_DUNGEON__VERIFIED.mention} role, what gives you access to '
            f'additional channels by typing `nya` at {CHANNEL__NEKO_DUNGEON__SYSTEM.mention}.\n'
            f'*You must be the member of the guild for at least 10 minutes and {client.mention} must be online '
            f'as well.*'
        ).add_field(
            '8. Advertisements',
            'Advertising other social medias, servers, communities or services in chat or in DM-s are disallowed.'
        ).add_field(
            '9. No political or religious topics.',
            'I do not say either that aliens exists, even tho they do.',
        ).add_field(
            '10. Alternative accounts',
            'Instant ban.'
        ).add_field(
            '11. Deep frying fumos',
            'Fumo frying is bannable offense.'
        )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


ABOUT = SLASH_CLIENT.interactions(None,
    name = 'about',
    description = 'My loli secret. Simpers only!',
    is_global = True,
)

@ABOUT.interactions(is_default=True)
async def description_(client, event):
    """What you should know about me, you perv!"""
    implementation = sys.implementation
    return Embed('About', f'Hello, I am {client.full_name} as you expected. What did you think, who am I?',
            color=COLOR__KOISHI_HELP) \
        .add_field('Library', f'[hata {__version__}]({LINK__HATA_GIT})', inline=True) \
        .add_field('Interpreter', (
            f'Python{implementation.version[0]}.{implementation.version[1]}'
            f'{"" if implementation.version[3]=="final" else " "+implementation.version[3]} {implementation.name}'
                ), inline=True) \
        .add_field('Support server', f'[{GUILD__NEKO_DUNGEON.name}]({INVITE__NEKO_DUNGEON.url})', inline=True) \
        .add_field('Clients', repr(len(CLIENTS)), inline=True) \
        .add_field('Guilds', repr(len(GUILDS)), inline=True) \
        .add_field('Users', repr(len(USERS)), inline=True) \
        .add_thumbnail(client.application.icon_url_as(size=128))


@ABOUT.interactions
async def invite_():
    """Invite to our beloved Neko Dungeon."""
    return INVITE__NEKO_DUNGEON.url


@ABOUT.interactions
async def git():
    """Link to my git repository."""
    return Embed(description=f'[Koishi repository]({LINK__KOISHI_GIT})', color=COLOR__KOISHI_HELP)


@ABOUT.interactions
async def hata():
    """Link to my wrapper's git repository."""
    return Embed(description=f'[hata repository]({LINK__HATA_GIT})', color=COLOR__KOISHI_HELP)


@ABOUT.interactions
async def slash():
    """Link to my wrapper's git repository."""
    return Embed(description=f'[slash]({LINK__HATA_SLASH})', color=COLOR__KOISHI_HELP)


@ABOUT.interactions
async def docs():
    """Sends a link to hata's documentation."""
    return Embed(description=f'[hata docs]({LINK__HATA_DOCS})', color=COLOR__KOISHI_HELP)


def docs_search_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    guild = event.channel.guild
    if guild is None:
        return False
    
    if guild.permissions_for(event_user).can_manage_messages:
        return True
    
    return False


@ABOUT.interactions
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
async def claimable():
    """A list of claimable roles in ND."""
    embed = Embed('Claimable roles:',
        f'Claim roles by typing a specific text at {CHANNEL__NEKO_DUNGEON__SYSTEM.mention}!',
        color=COLOR__KOISHI_HELP,
        ).add_field(
            ROLE__NEKO_DUNGEON__VERIFIED.name,
            f'Claim {ROLE__NEKO_DUNGEON__VERIFIED.mention} by typing `nya`!',
        ).add_field(
            ROLE__NEKO_DUNGEON__ANNOUNCEMENTS.name,
            f'Claim {ROLE__NEKO_DUNGEON__ANNOUNCEMENTS.mention} by typing `i meow`, or un-claim by `i not meow`!',
        ).add_field(
            ROLE__NEKO_DUNGEON__ELEVATED.name,
            f'Claim {ROLE__NEKO_DUNGEON__ELEVATED.mention} by typing `nekogirl`!'
            f'\n'
            f'*You must be in the guild for at least half year + have {ROLE__NEKO_DUNGEON__VERIFIED.mention} role*.',
        ).add_field(
            ROLE__NEKO_DUNGEON__NSFW_ACCESS.name,
            f'Claim {ROLE__NEKO_DUNGEON__NSFW_ACCESS.mention} by typing `i am horny`, or un-claim by `no sex`!'
            f'\n'
            f'*You must have {ROLE__NEKO_DUNGEON__VERIFIED.mention} role*.',
        )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


@ROLES.interactions
async def events():
    """Event related role information."""
    embed = Embed('Event roles', color=COLOR__KOISHI_HELP,
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
