__all__ = ('Marisa',)

import sys
from random import random
from time import perf_counter

from hata import (
    CHANNELS, Client, ClientWrapper, DiscordException, ERROR_CODES, Embed, GUILDS, IntentFlag, KOKORO, Locale,
    cchunkify
)
from hata.ext.commands_v2 import checks
from hata.ext.commands_v2.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import abort, set_permission
from hata.ext.slash.menus import Pagination
from scarletio import alchemy_incendiary, render_exception_into_async
from scarletio.utils.trace import render_exception_into

import config
from bot_utils.constants import (
    CHANNEL__SUPPORT__DEFAULT_TEST, COLOR__MARISA_HELP, DEFAULT_CATEGORY_NAME, GUILD__SUPPORT, PREFIX__MARISA,
    ROLE__SUPPORT__TESTER
)
from bot_utils.interpreter_v2 import Interpreter
from bot_utils.syncer import sync_request_command
from bot_utils.utils import category_name_rule, command_error


Marisa = Client(
    config.MARISA_TOKEN,
    secret = config.MARISA_SECRET,
    client_id = config.MARISA_ID,
    http_debug_options = 'canary',
    extensions = (
        'command_utils',
        'slash',
        'commands_v2',
        # 'solarlink',
    ),
    prefix = PREFIX__MARISA,
    default_category_name = DEFAULT_CATEGORY_NAME,
    category_name_rule = category_name_rule,
    translation_table = {
        Locale.english_us: {
            'cat-feeder': 'feed-ya-meow',
            'Feed the cat!': 'Owner hungry!'
        },
        Locale.english_gb: {
            'cat-feeder': 'feed-ya-meow',
            'Feed the cat!': 'Owner hungry!'
        },
    },
    shard_count = 2,
    intents = IntentFlag().update_by_keys(_17 = 1, _18 = 1, _19 = 1, _21 = 1),
    # assert_application_command_permission_missmatch_at = [GUILD__SUPPORT],
    # enforce_application_command_permissions = True,
)

'''
try:
    SOLARLINK_VOICE = Marisa.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None)
except BaseException as err:
    sys.stderr.write(f'Failed to connect to lavalink server: {err!r}.\n')
    SOLARLINK_VOICE = False

add_default_plugin_variables(SOLARLINK_VOICE = SOLARLINK_VOICE)
'''


Marisa.command_processor.create_category('TEST COMMANDS', checks = checks.owner_only())
Marisa.command_processor.create_category('VOICE', checks = checks.guild_only())
Marisa.command_processor.get_default_category().checks = checks.owner_only()

def marisa_help_embed_postprocessor(command_context, embed):
    if embed.color is None:
        embed.color = COLOR__MARISA_HELP
    
    embed.add_thumbnail(command_context.client.avatar_url)

"""
@Marisa.events
async def track_end(client, event):
    print(repr(event))

@Marisa.events
async def track_exception(client, event):
    print(repr(event))

@Marisa.events
async def track_start(client, event):
    print(repr(event))

@Marisa.events
async def track_stuck(client, event):
    print(repr(event))

@Marisa.events
async def player_websocket_closed(client, event):
    print(repr(event))
"""

Marisa.commands(
    SubterraneanHelpCommand(
        embed_postprocessor = marisa_help_embed_postprocessor,
    ),
    name = 'help',
    category = 'HELP',
)

@Marisa.command_processor.error
async def command_error_handler(ctx, exception):
    if ctx.guild is not GUILD__SUPPORT:
        return False
    
    into = [
        ctx.client.full_name,
        ' ignores an occurred exception at command ',
        repr(ctx.command),
        '\n\nMessage details:\nGuild: ',
        repr(ctx.guild),
        '\nChannel: ',
        repr(ctx.channel),
        '\nAuthor: ',
        ctx.author.full_name,
        ' (',
        repr(ctx.author.id),
        ')\nContent: ',
        repr(ctx.content),
        '\n```py\n'
    ]
    await render_exception_into_async(exception, into, loop=KOKORO)
    into.append('```')
    
    lines = ''.join(into).splitlines()
    into = None
    
    pages = []
    
    page_length = 0
    page_contents = []
    
    index = 0
    limit = len(lines)
    
    while True:
        if index == limit:
            embed = Embed(description = ''.join(page_contents))
            pages.append(embed)
            page_contents = None
            break
        
        line = lines[index]
        index = index + 1
        
        line_length = len(line)
        # long line check, should not happen
        if line_length > 500:
            line = line[:500]+'...\n'
            line_length = 504
        
        if page_length + line_length > 1997:
            if index == limit:
                # If we are at the last element, we don\'t need to shard up,
                # because the last element is always '```'
                page_contents.append(line)
                embed = Embed(description = ''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            page_contents.append('```')
            embed = Embed(description = ''.join(page_contents))
            pages.append(embed)
            
            page_contents.clear()
            page_contents.append('```py\n')
            page_contents.append(line)
            
            page_length = 6 + line_length
            continue
        
        page_contents.append(line)
        page_length += line_length
        continue
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(ctx.client, ctx.channel, pages)
    return True


Marisa.commands(command_error, checks = [checks.is_guild(GUILD__SUPPORT)])

ALL = ClientWrapper()

@ALL.events
async def ready(client):
    sys.stdout.write(f'{client:f} logged in.\n')
    sys.stdout.write(
        f'guild count: {len(GUILDS)}\n'
        f'channel count: {len(CHANNELS)}\n'
    )


async def execute_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed(
        'execute',
        (
            'Use an interpreter trough me :3\n'
            'Usages:\n'
            f'{prefix}execute # code goes here\n'
            '# code goes here\n'
            '# code goes here\n'
            '\n'
            f'{prefix}execute\n'
            '```\n'
            '# code goes here\n'
            '# code goes here\n'
            '```\n'
            '*not code*\n'
            '\n'
            '... and many more ways.'
        ),
        color = COLOR__MARISA_HELP,
    ).add_footer(
        'Owner only!'
    )

Marisa.commands(
    Interpreter(locals().copy()),
    name = 'execute',
    description = execute_description,
    category = 'UTILITY',
    checks = [
        checks.owner_only(),
    ],
)

Marisa.commands(sync_request_command, name = 'sync', category='UTILITY', checks=[checks.owner_only()])

@ALL.events(overwrite = True)
async def error(client, name, err):
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await KOKORO.run_in_executor(alchemy_incendiary(render_exception_into, (err, extracted)))
    else:
        if not isinstance(err, str):
            err = repr(err)
        
        extracted.append(err)
        extracted.append('\n')
    
    extracted = ''.join(extracted).split('\n')
    for chunk in cchunkify(extracted, lang = 'py'):
        await client.message_create(CHANNEL__SUPPORT__DEFAULT_TEST, chunk)



# You might wanna add `-tag`-s to surely avoid nsfw pictures
SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='

# Use a cache to avoid repeated requests.
# Booru also might ban ban you for a time if you do too much requests.
IMAGE_URL_CACHE = {}

@Marisa.interactions(guild = GUILD__SUPPORT)
async def retardify(client, event,
    text : ('str', 'Some text to retardify.'),
):
    """Translates the given text to retard language."""
    if text:
        description_parts = []
        chance = 0.5
        
        for char in text:
            if random() > chance:
                if chance > 0.5:
                    chance = 1.0 - (chance * 0.5)
                else:
                    chance = 0.5
                
                char = char.lower()
            else:
                if chance <= 0.5:
                    chance = chance * 0.5
                else:
                    chance = 0.5
                
                char = char.upper()
            
            description_parts.append(char)
        
        description = ''.join(description_parts)
    else:
        description = 'Nothing to retardify.'
    
    embed = Embed(description = description)
    user = event.user
    embed.add_author(user.full_name, user.avatar_url)
    
    await client.interaction_response_message_create(event, embed = embed, allowed_mentions = None)


Marisa@set_permission(GUILD__SUPPORT, ('role',                     0), False)
Marisa@set_permission(GUILD__SUPPORT,           ROLE__SUPPORT__TESTER,  True)
Marisa@set_permission(GUILD__SUPPORT, ('channel',                  0), False)
Marisa@set_permission(GUILD__SUPPORT, ('channel', 648137901632126996), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 890686019811307560), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 791260426780278785), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 790028318237261864), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 776864383183749141), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 830877889322811413), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 403584215855267853), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 557187647831932938), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 654932659620937748), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 533609128288059392), True )
Marisa@set_permission(GUILD__SUPPORT, ('channel', 918901494839922689), True )


@Marisa.interactions(guild = GUILD__SUPPORT)
async def debug_command(client, event,
    command_name: (str, 'The command\'s name.')
):
    """Gets debug information about the given command."""
    if not client.is_owner(event.user):
        abort('Owner only.')
    
    if not command_name:
        abort('Empty command name.')
    
    application_commands = await client.application_command_guild_get_all(GUILD__SUPPORT)
    for application_command in application_commands:
        if application_command.name == command_name:
            break
    else:
        abort('Command could not be found.')
    
    try:
        permission = await client.application_command_permission_get(GUILD__SUPPORT, application_command)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_application_command_permissions:
            permission = None
        else:
            raise
    
    text_parts = [
        '**Application command**:\n'
        'Name : `', application_command.name, '`\n'
        'Id : `', repr(application_command.id), '`\n'
        'Allow in dm : `', repr(application_command.allow_in_dm), '`\n'
        'required permissions : `', repr(application_command.required_permissions), '`\n'
        'target type : `', repr(application_command.target_type.name), '`\n'
        '**Permission overwrites**:\n'
    ]
    
    if permission is None:
        permission_overwrites = None
    else:
        permission_overwrites = permission.permission_overwrites
    
    if permission_overwrites is None:
        text_parts.append('*none*')
    else:
        for index, permission_overwrite in enumerate(permission_overwrites):
            text_parts.append(repr(index))
            text_parts.append('.: type: `')
            text_parts.append(permission_overwrite.target_type.name)
            text_parts.append('`; id: `')
            text_parts.append(repr(permission_overwrite.target_id))
            
            target = permission_overwrite.target
            if target is None:
                target_name = '*unknown*'
            else:
                target_name = permission_overwrite.target.name
            if target_name:
                text_parts.append('`; name: `')
                text_parts.append(target_name)
            
            text_parts.append('`; allowed: `')
            text_parts.append(repr(permission_overwrite.allow))
            text_parts.append('`\n')
    
    return ''.join(text_parts)


now = perf_counter()

@Marisa.events
async def ready(client):
    print(perf_counter() - now)
    Marisa.events.remove(ready)


@Marisa.commands
@checks.owner_only()
async def count_message_fields(client, message):
    
    message_count = 0
    
    field_count_activity = 0
    field_count_application = 0
    field_count_application_id = 0
    field_count_attachments = 0
    field_count_components = 0
    field_count_content = 0
    field_count_mentioned_channels_cross_guild = 0
    field_count_referenced_message = 0
    field_count_deleted = 0
    field_count_edited_at = 0
    field_count_embeds = 0
    field_count_everyone_mention = 0
    field_count_interaction = 0
    field_count_nonce = 0
    field_count_pinned = 0
    field_count_reactions = 0
    field_count_mentioned_role_ids = 0
    field_count_stickers = 0
    field_count_thread = 0
    field_count_tts = 0
    field_count_mentioned_users = 0
    
    total_fields_by_count = {}
    
    async for message in await client.message_iterator(message.channel):
        message_count += 1
        total_fields = 0
        
        if message.has_activity():
            field_count_activity += 1
            total_fields += 1
        
        if message.has_application():
            field_count_application += 1
            total_fields += 1
        
        if message.has_application_id():
            field_count_application_id += 1
            total_fields += 1
        
        if message.has_attachments():
            field_count_attachments += 1
            total_fields += 1
        
        if message.has_components():
            field_count_components += 1
            total_fields += 1
        
        if message.has_content():
            field_count_content += 1
            total_fields += 1
        
        if message.has_mentioned_channels_cross_guild():
            field_count_mentioned_channels_cross_guild += 1
            total_fields += 1
        
        if message.has_referenced_message():
            field_count_referenced_message += 1
            total_fields += 1
        
        if message.has_deleted():
            field_count_deleted += 1
            total_fields += 1
        
        if message.has_edited_at():
            field_count_edited_at += 1
            total_fields += 1
        
        if message.has_embeds():
            field_count_embeds += 1
            total_fields += 1
        
        if message.has_everyone_mention():
            field_count_everyone_mention += 1
            total_fields += 1
        
        if message.has_interaction():
            field_count_interaction += 1
            total_fields += 1
        
        if message.has_nonce():
            field_count_nonce += 1
            total_fields += 1
        
        if message.has_pinned():
            field_count_pinned += 1
            total_fields += 1
        
        if message.has_reactions():
            field_count_reactions += 1
            total_fields += 1
        
        if message.has_mentioned_role_ids():
            field_count_mentioned_role_ids += 1
            total_fields += 1
        
        if message.has_stickers():
            field_count_stickers += 1
            total_fields += 1
        
        if message.has_thread():
            field_count_thread += 1
            total_fields += 1
        
        if message.has_tts():
            field_count_tts += 1
            total_fields += 1
        
        if message.has_mentioned_users():
            field_count_mentioned_users += 1
            total_fields += 1
        
        try:
            by_count = total_fields_by_count[total_fields]
        except KeyError:
            by_count = 1
        else:
            by_count += 1
        
        total_fields_by_count[total_fields] = by_count
        
        if message_count == 1000:
            break
    
    description_parts = []
    
    fields_array = [
        (field_count_activity, 'activity'),
        (field_count_application, 'application'),
        (field_count_application_id, 'application_id'),
        (field_count_attachments, 'attachments'),
        (field_count_components, 'components'),
        (field_count_content, 'content'),
        (field_count_mentioned_channels_cross_guild, 'mentioned_channels_cross_guild'),
        (field_count_referenced_message, 'referenced_message'),
        (field_count_deleted, 'deleted'),
        (field_count_edited_at, 'edited_at'),
        (field_count_embeds, 'embeds'),
        (field_count_everyone_mention, 'everyone_mention'),
        (field_count_interaction, 'interaction'),
        (field_count_nonce, 'nonce'),
        (field_count_pinned, 'pinned'),
        (field_count_reactions, 'reactions'),
        (field_count_mentioned_role_ids, 'mentioned_role_ids'),
        (field_count_stickers, 'stickers'),
        (field_count_thread, 'thread'),
        (field_count_tts, 'tts'),
        (field_count_mentioned_users, 'mentioned_users'),
    ]
    
    fields_array.sort(reverse=True)
    
    for field_count, field_name in fields_array:
        description_parts.append('**')
        description_parts.append(field_name)
        description_parts.append('**: ')
        description_parts.append(repr(field_count))
        description_parts.append('\n')
    
    description_parts.append('\n')
    
    total_fields_array = list(total_fields_by_count.items())
    total_fields_array.sort(reverse=True)
    
    for total_fields, message_amount in total_fields_array:
        description_parts.append('**')
        description_parts.append(repr(total_fields))
        description_parts.append(' fields**: ')
        description_parts.append(repr(message_amount))
        description_parts.append('\n')
    
    description_parts.append('\n')
    
    if message_count:
        total_total_fields = 0
        for total_fields, message_amount in total_fields_array:
            total_total_fields += total_fields * message_amount
        
        average_fields = total_total_fields / message_count
    else:
        average_fields = 0.0
    
    description_parts.append('**Total messages**: ')
    description_parts.append(repr(message_count))
    description_parts.append('\n**Average fields**:' )
    description_parts.append(average_fields.__format__('.02f'))
    description_parts.append('\n**Total fields**: 22 (including cache)')
    
    return ''.join(description_parts)


@Marisa.commands
async def shutdown():
    await Marisa.stop()
