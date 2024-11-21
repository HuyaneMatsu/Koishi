__all__ = ()

import sys
from os import listdir as list_directory
from os.path import isdir as is_directory, isfile as is_file, join as join_paths
from platform import platform as get_platform
from random import choice

from hata import (
    BUILTIN_EMOJIS, CHANNELS, CLIENTS, Client, EMOJIS, Embed, GUILDS, InteractionType, MESSAGES, ROLES, STICKERS, USERS,
    __package__ as LIBRARY_NAME, __version__ as LIBRARY_VERSION, elapsed_time
)
from hata.ext.slash import Button, InteractionResponse, Row, abort

from ..bot_utils.constants import (
    COLOR__KOISHI_HELP, GUILD__ORIN_PARTY_HOUSE, INVITE__SUPPORT, PATH__KOISHI, STARTUP, URL__KOISHI_TOP_GG
)
from ..bot_utils.cpu_info import CpuUsage, PROCESS
from ..bot_utils.headers import get_header_for
from ..bots import FEATURE_CLIENTS, MAIN_CLIENT


@FEATURE_CLIENTS.events(name = 'interaction_create')
class interaction_counter:
    application_command = 0
    total = 0
    
    async def __new__(cls, client, interaction_event):
        cls.application_command += (interaction_event.type is InteractionType.application_command)
        cls.total += 1


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
    f'{LIBRARY_NAME} {LIBRARY_VERSION}\n'
    f'```'
)

UPTIME_TITLE = f'{BUILTIN_EMOJIS["green_circle"].as_emoji} Uptime'

PLATFORM_FIELD_VALUE = (
    f'```\n'
    f'{get_platform()}\n'
    f'```'
)

CUSTOM_ID_ABOUT_CLOSE = 'about.close'


def iter_about_components(client):
    yield Button(
        'Invite me!',
        url = (
            f'https://discord.com/oauth2/authorize'
            f'?client_id={client.application.id}'
            f'&scope=bot%20applications.commands'
        ),
    )
    
    yield Button(
        'Install me!',
        url = (
            f'https://discord.com/oauth2/authorize'
            f'?client_id={client.application.id}'
            f'&scope=applications.commands'
            f'&integration_type=1'
        ),
    )
    
    yield Button(
        'Support server',
         url = INVITE__SUPPORT.url,
    )
    
    # yield Button(
    #     'Source code',
    #     url = URL__KOISHI_GIT,
    # )
    
    if client is MAIN_CLIENT:
        yield Button(
            'Vote for me!',
            url = URL__KOISHI_TOP_GG,
        )
    
    yield Button(
        'Close',
        BUILTIN_EMOJIS['x'],
        custom_id = CUSTOM_ID_ABOUT_CLOSE,
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
        
        if is_directory(path):
            line_break_count += count_lines_of(path)
            continue
    
    return line_break_count


LINE_COUNT_FIELD_VALUE = (
    f'```\n'
    f'{count_lines_of(PATH__KOISHI):,}\n'
    f'```'
)


KOISHI_JOKES = (
    ('Shrimps', 'fried'),
    ('Apples', 'peeled'),
    ('Okuu', 'beatboxing'),
    ('Fishing rods', 'wings*'),
    ('Orin', 'dancing'),
    ('We like', 'older woman'),
    ('KFC', 'Koishi Fried Chicken'),
    ('Koishi', '"Not thinking is fun!"'),
)


async def render_about_generic(client, event):
    """
    Renders a generic about embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        None,
        get_header_for(client),
        color = COLOR__KOISHI_HELP,
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
    
    field_title, field_value = choice(KOISHI_JOKES)
    
    embed.add_field(
        field_title,
        (
            f'```\n'
            f'{field_value}\n'
            f'```'
        ),
    ).add_field(
        'Guild count',
        (
            f'```\n'
            f'{len(client.guilds)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Used commands',
        (
            f'```\n'
            f'{interaction_counter.application_command}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Total interactions',
        (
            f'```\n'
            f'{interaction_counter.total}\n'
            f'```'
        ),
        inline = True,
    )
    
    return embed


async def render_about_js(client, event):
    """
    Renders a javascript about because why not.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        None,
        get_header_for(client),
        color = COLOR__KOISHI_HELP,
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
        'Library',
        (
            f'```\n'
            f'discord.js\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Version',
        (
            f'```\n'
            f'14.6.0\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Line count',
        LINE_COUNT_FIELD_VALUE,
    )
    
    guild_id = event.guild_id
    if guild_id:
        command_count = client.slasher.get_guild_command_count(guild_id)
        command_count_with_sub_commands = client.slasher.get_guild_command_count_with_sub_commands(guild_id)
    else:
        command_count = 0
        command_count_with_sub_commands = 0
    
    command_count += client.slasher.get_global_command_count()
    command_count_with_sub_commands += client.slasher.get_global_command_count_with_sub_commands()
    
    command_count = min(command_count, 105)
    
    embed.add_field(
        'Global command count',
        (
            f'```\n'
            f'{command_count}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Including sub commands',
        (
            f'```\n'
            f'{command_count_with_sub_commands}\n'
            f'```'
        ),
        inline = True
    )
        
    field_title = 'Koishi'
    field_value = 'The bot who borrows your fishing rods and eats your shrimp fry.'
    
    embed.add_field(
        field_title,
        (
            f'```\n'
            f'{field_value}\n'
            f'```'
        ),
    ).add_field(
        'Guild count',
        (
            f'```\n'
            f'{len(client.guilds)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Used commands',
        (
            f'```\n'
            f'{interaction_counter.application_command}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Total interactions',
        (
            f'```\n'
            f'{interaction_counter.total}\n'
            f'```'
        ),
        inline = True,
    )
    
    return embed


async def render_about_cache(client, event):
    """
    Renders a cache info about embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        color = COLOR__KOISHI_HELP,
    ).add_field(
        'Emojis',
        (
            f'```\n'
            f'{len(EMOJIS)}\n'
            f'```'
        ),
        inline = True
    ).add_field(
        'Guilds',
        (
            f'```\n'
            f'{len(GUILDS)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Roles',
        (
            f'```\n'
            f'{len(ROLES)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Stickers',
        (
            f'```\n'
            f'{len(STICKERS)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Channels',
        (
            f'```\n'
            f'{len(CHANNELS)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Messages',
        (
            f'```\n'
            f'{len(MESSAGES)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Users',
        (
            f'```\n'
            f'{len(USERS)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Clients',
        (
            f'```\n'
            f'{len(CLIENTS)}\n'
            f'```'
        ),
        inline = True,
    )
    
    return embed


ABOUT_FIELD_NAME_GENERIC = 'generic'
ABOUT_FIELD_NAME_CACHE = 'cache'

ABOUT_FIELD_CHOICES = [
    ABOUT_FIELD_NAME_GENERIC,
    ABOUT_FIELD_NAME_CACHE,
]

ABOUT_FIELD_NAME_TO_RENDERER = {
    ABOUT_FIELD_NAME_GENERIC: render_about_generic,
    ABOUT_FIELD_NAME_CACHE: render_about_cache,
}


@FEATURE_CLIENTS.interactions(is_global = True)
async def about(
    client,
    event,
    field: (ABOUT_FIELD_CHOICES, 'Choose a field!') = ABOUT_FIELD_NAME_GENERIC,
):
    """
    My secrets and stats. Simps only!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    try:
        field_renderer = ABOUT_FIELD_NAME_TO_RENDERER[field]
    except KeyError:
        return abort(f'Unknown field: {field!r}.')
    
    if (field_renderer is render_about_generic) and (event.guild is GUILD__ORIN_PARTY_HOUSE):
        field_renderer = render_about_js
    
    embed = await field_renderer(client, event)
    return InteractionResponse(
        embed = embed,
        components = Row(*iter_about_components(client)),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ABOUT_CLOSE)
async def about_close(client, event):
    """
    Closes the about message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    if event.user_permissions.manage_messages or event.message.interaction.user_id == event.user_id:
        await client.interaction_response_message_delete(event)
    
    else:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
