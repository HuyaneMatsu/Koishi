import sys
from functools import partial as partial_func
from platform import platform as get_platform
from os.path import join as join_paths, isdir as is_folder, isfile as is_file
from os import listdir as list_directory

from hata import CLIENTS, USERS, GUILDS, Embed, Client, __version__, Emoji, elapsed_time, BUILTIN_EMOJIS, __package__
from hata.ext.slash.menus import Pagination, Closer
from hata.ext.slash import InteractionResponse, Button, Row

from bot_utils.shared import LINK__KOISHI_GIT, LINK__HATA_GIT, INVITE__NEKO_DUNGEON, GUILD__NEKO_DUNGEON, \
    LINK__HATA_DOCS, LINK__PASTE, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, COLOR__KOISHI_HELP, ROLE__NEKO_DUNGEON__ELEVATED, \
    ROLE__NEKO_DUNGEON__VERIFIED, CHANNEL__NEKO_DUNGEON__SYSTEM, LINK__HATA_SLASH, ROLE__NEKO_DUNGEON__NSFW_ACCESS, \
    ROLE__NEKO_DUNGEON__EVENT_MANAGER, ROLE__NEKO_DUNGEON__EVENT_WINNER, ROLE__NEKO_DUNGEON__EVENT_PARTICIPANT, \
    EMOJI__HEART_CURRENCY, ROLE__NEKO_DUNGEON__HEART_BOOST, STARTUP, PATH__KOISHI
from bot_utils. cpu_info import CpuUsage, PROCESS

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
    
    interpreter_info_parts = ['```\n']
    
    interpreter_info_parts.append('Python')
    interpreter_info_parts.append(repr(main_version_number))
    interpreter_info_parts.append('.')
    interpreter_info_parts.append(repr(sub_version_number))
    
    if release != 'final':
        interpreter_info_parts.append(' ')
        interpreter_info_parts.append(release)
    
    interpreter_info_parts.append(' ')
    interpreter_info_parts.append(implementation.name)
    
    interpreter_info_parts.append('\n```')
    
    return ''.join(interpreter_info_parts)


PYTHON_VERSION_FIELD_VALUE = create_interpreter_info()
LIBRARY_VERSION_FIELD_VALUE = (
    f'```\n'
    f'{__package__} {__version__}\n'
    f'```'
)

UPTIME_TITLE = f'{BUILTIN_EMOJIS["green_circle"].as_emoji} Uptime'

PLATFORM_FIELD_VALUE = (
    f'```\n'
    f'{get_platform()}\n'
    f'```'
)

ABOUT_COMPONENTS = Row(
    Button(
        'Library',
        url = LINK__HATA_GIT,
    ),
    Button(
        'Source code',
        url = LINK__KOISHI_GIT,
    ),
    Button(
        'Invite me!',
        url = (
            f'https://discord.com/oauth2/authorize?client_id={SLASH_CLIENT.application.id}&scope=bot%20'
            f'applications.commands'
        ),
    ),
    Button(
        'Support server',
        url = INVITE__NEKO_DUNGEON.url,
    ),
)


def count_lines_of(directory_path):
    line_break_count = 0
    
    for name in list_directory(directory_path):
        path = join_paths(directory_path, name)
        if is_file(path):
            if name.endswith(('.py', '.txt', '.json', '.md')): # Which files should we count?
                with open(path, 'r') as file:
                    line_break_count += file.read().count('\n')
            
            continue
        
        if is_folder(path):
            line_break_count += count_lines_of(path)
            continue
    
    return line_break_count


LINE_COUNT_FIELD_VALUE = (
    f'```\n'
    f'{count_lines_of(PATH__KOISHI):,}\n'
    f'```'
)


@SLASH_CLIENT.interactions(is_global=True)
async def about(client, event):
    """My loli secret. Simpers only!"""
    embed = Embed(
        None,
        (
            '```\n'
            ' _   __      _     _     _ \n'
            '| | / /     (_)   | |   (_)\n'
            '| |/ /  ___  _ ___| |__  _ \n'
            '|    \ / _ \| / __| \'_ \| |\n'
            '| |\  \ (_) | \__ \ | | | |\n'
            '\_| \_/\___/|_|___/_| |_|_|\n'
            '```'
        ),
        color = COLOR__KOISHI_HELP,
        timestamp = event.created_at,
    ).add_author(
        client.avatar_url,
        client.full_name,
    ).add_footer(
        f'Requested by {event.user.full_name}',
        icon_url = event.user.avatar_url,
    ).add_field(
        UPTIME_TITLE,
        (
            f'```\n'
            f'{elapsed_time(STARTUP)}\n'
            f'```'
        )
    ).add_field(
        'Hosting',
        PLATFORM_FIELD_VALUE,
    )
    
    if (CpuUsage is not None):
        cpu_usage = await CpuUsage()
        embed.add_field(
            'CPU usage',
            (
                f'```\n'
                f'{cpu_usage.cpu_percent:.2f}%\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'CPU frequency',
            (
                f'```\n'
                f'{cpu_usage.average_cpu_frequency:.2f} MHz\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Memory usage',
            (
                f'```\n'
                f'{(PROCESS.memory_info().rss / (1 << 20)):.2f} MB\n'
                f'```'
            ),
            inline = True,
        )
    
    embed.add_field(
        'Interpreter',
        PYTHON_VERSION_FIELD_VALUE,
        inline = True,
    ).add_field(
        'Library',
        LIBRARY_VERSION_FIELD_VALUE,
        inline = True,
    ).add_field(
        'Line count',
        LINE_COUNT_FIELD_VALUE,
    )
    
    embed.add_field(
        'Global command count',
        (
            f'```\n'
            f'{client.slasher.get_global_command_count()}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Including sub commands',
        (
            f'```\n'
            f'{client.slasher.get_global_command_count_with_sub_commands()}\n'
            f'```'
        ),
        inline = True
    )
    
    guild_id = event.guild_id
    if guild_id:
        guild_command_count = client.slasher.get_guild_command_count(guild_id)
        
        if guild_command_count:
            embed.add_field(
                'Guild specific commands',
                (
                    f'```\n'
                    f'{guild_command_count}\n'
                    f'```'
                ),
                inline = True
            )
    
    embed.add_field(
        'Shrimps',
        (
            '```\n'
            'fried\n'
            '```'
        ),
    ).add_field(
        'Guild count',
        (
            f'```\n'
            f'{len(GUILDS)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Client count',
        (
            f'```\n'
            f'{len(CLIENTS)}\n'
            f'```'
        ),
        inline = True,
    )
    
    return InteractionResponse(
        embed = embed,
        components = ABOUT_COMPONENTS,
    )


def docs_search_pagination_check(user, event):
    if user is event.user:
        return True
    
    if event.user_permissions.can_manage_messages:
        return True
    
    return False

COMMAND_LIST_EMBED = Embed(
    'Help',
    color = COLOR__KOISHI_HELP,
).add_field(
    'Administration',
    '`clear`, `ban`, `bans`, `emoji-role`, `invite-create`, `invites`, `is-banned`',
    inline = True,
).add_field(
    'Anime',
    '`anime`, `character`, `fine-anime`, `find-character`, `find-manga`, `manga`',
    inline = True,
).add_field(
    'Actions',
    (
        '`bite`, `blush`, `bully`, `cringe`, `cry`, `dance`, `glomp`, `handhold`, `happy`, `highfive`, `hug`, `kill`, '
        '`kiss`, `lick`, `nom`, `pat`, `poke`, `slap`, `smile`, `smug`, `wave`, `wink`, `yeet`'
    ),
    inline = True,
).add_field(
    'Economy',
    '`daily`, `heart-shop`, `hearts`, `top-list`',
    inline = True,
).add_field(
    'Fun',
    '`meme`, `message-me`, `minesweeper`, `paranoia`, `random`, `rate`, `roll`, `sex`, `trivia`, `yuno`',
    inline = True,
).add_field(
    'Games',
    '`21`, `ds`, `xox`',
    inline = True,
).add_field(
    'Help',
    '`about`, `help`',
    inline = True,
).add_field(
    'Marriage',
    (
        '`love`\n\n'
        'Coming soon:\n'
        '```\n'
        'buy-waifu-slot, divorce, propose, proposals, waifu-info\n'
        '```'
    ),
    inline = True,
).add_field(
    'Utility',
    (
        '`avatar`, `calc`, `color`, `guild`, `guild-icon`, `id`, `is-to-datetime`, `now-as-id`, `ping`, `rawr`, '
        '`role`, `roles`, `show-emoji`, `user`, `welcome-screen`'
    ),
    inline = True,
).add_field(
    'Waifus',
    '`nsfw-booru`, `safe-booru`, `touhou-character`, `waifu`',
    inline = True,
)

# `status`,
# `escape`,

@SLASH_CLIENT.interactions(is_global=True)
async def help_(client, event):
    """Lists my commands."""
    return COMMAND_LIST_EMBED


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
