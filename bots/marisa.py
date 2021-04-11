# -*- coding: utf-8 -*-
import sys
from random import random, choice, shuffle
from time import perf_counter
from math import ceil
from collections import deque, OrderedDict
from html import unescape as html_unescape
from functools import partial as partial_func
from datetime import datetime, timedelta
from hata.discord.rate_limit import parse_date_to_datetime

from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

from hata import Embed, Client, parse_emoji, DATETIME_FORMAT_CODE, elapsed_time, id_to_time, sleep, KOKORO, cchunkify, \
    alchemy_incendiary, RoleManagerType, ICON_TYPE_NONE, BUILTIN_EMOJIS, Status, ChannelText, ChannelVoice, Lock, \
    ChannelCategory, ChannelStore, ChannelThread, time_to_id, imultidict, DiscordException, ERROR_CODES, CHANNELS, \
    MESSAGES, parse_message_reference, parse_emoji, istr, Future, LOOP_TIME, parse_rdelta, parse_tdelta, \
    ApplicationCommandPermissionOverwriteType, ClientWrapper
from hata.ext.commands import setup_ext_commands, checks, Pagination, wait_for_reaction
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import setup_ext_slash, SlashResponse, abort, set_permission
from hata.backend.futures import render_exc_to_list
from hata.backend.quote import quote
from hata.discord.http import LIB_USER_AGENT
from hata.backend.headers import USER_AGENT, DATE

from bot_utils.shared import category_name_rule, DEFAULT_CATEGORY_NAME, PREFIX__MARISA, COLOR__MARISA_HELP, \
    command_error, GUILD__NEKO_DUNGEON, CHANNEL__NEKO_DUNGEON__DEFAULT_TEST, ROLE__NEKO_DUNGEON__TESTER
from bot_utils.syncer import sync_request_command
from bot_utils.interpreter import Interpreter
from bot_utils.tools import choose, Cell

Marisa : Client

setup_ext_commands(Marisa, PREFIX__MARISA, default_category_name=DEFAULT_CATEGORY_NAME,
    category_name_rule=category_name_rule)

setup_ext_slash(Marisa)

Marisa.command_processer.create_category('TEST COMMANDS', checks=checks.owner_only())
Marisa.command_processer.create_category('VOICE', checks=checks.guild_only())

Marisa.commands(SubterraneanHelpCommand(COLOR__MARISA_HELP), 'help', category='HELP')

Marisa.commands(command_error, checks=[checks.is_guild(GUILD__NEKO_DUNGEON)])

ALL = ClientWrapper()

@ALL.events
async def ready(client):
    sys.stdout.write(f'{client:f} logged in.\n')


async def execute_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('execute', (
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
            ), color=COLOR__MARISA_HELP).add_footer(
            'Owner only!')

Marisa.commands(Interpreter(locals().copy()), name='execute', description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])

Marisa.commands(sync_request_command, name='sync', category='UTILITY', checks=[checks.owner_only()])


@ALL.events(overwrite=True)
async def error(client, name, err):
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
            ]
    
    if isinstance(err, BaseException):
        await KOKORO.run_in_executor(alchemy_incendiary(render_exc_to_list, (err, extracted)))
    else:
        if not isinstance(err, str):
            err = repr(err)
        
        extracted.append(err)
        extracted.append('\n')
    
    extracted = ''.join(extracted).split('\n')
    for chunk in cchunkify(extracted, lang='py'):
        await client.message_create(CHANNEL__NEKO_DUNGEON__DEFAULT_TEST, chunk)


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def cookie(client, event,
        user : ('user', 'To who?') = None,
            ):
    """Gifts a cookie!"""
    if user is None:
        source_user = client
        target_user = event.user
    else:
        source_user = event.user
        target_user = user
    
    return Embed(description=f'{source_user:f} just gifted a cookie to {target_user:f} !')


DO_THINGS_CHOICES = [
    'I adopted Reimu.',
    'I did not steal anyone\'s dress!',
    'I have some mushrooms under my skirt, do you want some?',
    'Suwako\'s secret family technique is lovely.',
    'Suwako used her family technique on Sanae, who shared it with Reimu.',
    'Saw once Yukari\'s animal abuse, still having wet dreams about it.',
    'Reimu\'s armpits, yeeaaa...',
    'Have you heard of Izaoyi love-shop?',
        ]

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def do_things(client, event):
    """I will do things!"""
    yield '*Doing things*'
    await sleep(1.0+random()*4.0, KOKORO)
    yield choose(DO_THINGS_CHOICES)


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON, show_for_invoking_user_only=True)
async def perms(client, event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        content = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        content = '*none*'
    
    return content


@Marisa.interactions
async def ping(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@Marisa.interactions(is_global=True)
async def enable_ping(client, event,
        allow: ('bool', 'Enable?')=True,
            ):
    """Enables the ping command in your guild."""
    guild = event.guild
    if guild is None:
        return Embed('Error', 'Guild only command.')
    
    if not event.user_permissions.can_administrator:
        return Embed('Permission denied', 'You must have administrator permission to use this command.')
    
    application_commands = await client.application_command_guild_get_all(guild)
    for application_command in application_commands:
        # If you are not working with overlapping names, a name check should be enough.
        if application_command.name == ping.name:
            command_present = True
            break
    else:
        command_present = False
    
    if allow:
        if command_present:
            content = 'The command is already present.'
        else:
            await client.application_command_guild_create(guild, ping.get_schema())
            content = 'The command has been added.'
    else:
        if command_present:
            await client.application_command_guild_delete(guild, application_command)
            content = 'The command has been disabled.'
        else:
            content = 'The command is not present.'
    
    return Embed('Success', content)

# You might wanna add `-tag`-s to surely avoid nsfw pictures
SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='

# Use a cache to avoid repeated requests.
# Booru also might ban ban you for a time if you do too much requests.
IMAGE_URL_CACHE = {}

async def get_image_embed(client, tags, name, color):
    image_urls = IMAGE_URL_CACHE.get(tags)
    if image_urls is None:
        # Yield to acknowledge the event.
        yield
        
        # Request image information
        async with client.http.get(SAFE_BOORU+tags) as response:
            if response.status != 200:
                abort('Safe-booru unavailable')
            
            result = await response.read()
        
        # Read response and get image urls.
        soup = BeautifulSoup(result, 'lxml')
        image_urls = [post['file_url'] for post in soup.find_all('post')]
        
        if not image_urls:
            abort('No images found.\nPlease try again later.')
        
        # If we received image urls, cache them
        IMAGE_URL_CACHE[tags] = image_urls
    
    image_url = choice(image_urls)
    yield SlashResponse(Embed(name, color=color, url=image_url).add_image(image_url), show_for_invoking_user_only=False)
    return

SCARLET = Marisa.interactions(None, name='scarlet', description='Scarlet?', guild=GUILD__NEKO_DUNGEON)

@SCARLET.interactions(show_for_invoking_user_only=True)
async def flandre(client, event):
    """Flandre!"""
    return get_image_embed(client, 'flandre_scarlet', 'Scarlet Flandre', 0xdc143c)

@SCARLET.interactions(show_for_invoking_user_only=True)
async def remilia(client, event):
    """Remilia!"""
    return get_image_embed(client, 'remilia_scarlet', 'Scarlet Remilia', 0x9400d3)

@SCARLET.interactions(is_default=True, show_for_invoking_user_only=True)
async def devil(client, event):
    """Flandre & Remilia!"""
    return get_image_embed(client, 'flandre_scarlet+remilia_scarlet', 'Scarlet Flandre & Remilia', 0xa12a2a)

'''
class Action:
    __slots__ = ('action_name', 'embed_color', )
    def __init__(self, action_name, embed_color):
        self.action_name = action_name
        self.embed_color = embed_color
    
    async def __call__(self, client, event,
            user : ('user', 'Who?') = None,
                ):
        if user is None:
            source_user = client
            target_user = event.user
        else:
            source_user = event.user
            target_user = user
        
        return Embed(description=f'{source_user:f} {self.action_name}s {target_user:f} !', color=self.embed_color)

for action_name, embed_color in (('pat', 0x325b34), ('hug', 0xa4b51b), ('lick', 0x7840c3), ('slap', 0xdff1dc),):
    Marisa.interactions(Action(action_name, embed_color),
        name = action_name,
        description = f'Do you want some {action_name}s, or to {action_name} someone?',
        guild = GUILD__NEKO_DUNGEON,
            )

# Cleanup
del action_name, embed_color
'''

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def kaboom(client, event):
    """Kabooom!!"""
    await client.interaction_response_message_create(event)
    
    messages = []
    for x in reversed(range(1, 4)):
        message = await client.interaction_followup_message_create(event, x)
        messages.append(message)
        await sleep(1.0)
    
    await client.interaction_followup_message_create(event, 'KABOOM!!')
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def kaboom_mixed(client, event):
    """Kabooom!!"""
    yield
    
    messages = []
    for x in reversed(range(1, 4)):
        message = yield str(x)
        messages.append(message)
        await sleep(1.0)
    
    yield 'KABOOM!!'
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)



@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
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
                    chance = 1.0-(chance*0.5)
                else:
                    chance = 0.5
                
                char = char.lower()
            else:
                if chance <= 0.5:
                    chance = chance*0.5
                else:
                    chance = 0.5
                
                char = char.upper()
            
            description_parts.append(char)
        
        description = ''.join(description_parts)
    else:
        description = 'Nothing to retardify.'
    
    embed = Embed(description=description)
    user = event.user
    embed.add_author(user.avatar_url, user.full_name)
    
    await client.interaction_response_message_create(event, embed=embed, allowed_mentions=None)
    
@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def test_channel_and_role(client, event,
        user : ('user', 'Please input a user') = None,
        channel : ('channel', 'Please input a channel') = None,
        role : ('role', 'Please input a role') = None,
            ):
    """Testing entities."""
    return \
        f'resolved_users = {event.resolved_users!r}\n' \
        f'resolved_channels = {event.resolved_channels!r}\n' \
        f'resolved_roles = {event.resolved_roles!r}\n' \
        f'user = {user!r}\n' \
        f'channel = {channel!r}\n' \
        f'role = {role!r}'


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON, show_for_invoking_user_only=True)
async def invoking_user_only(client, event):
    """SHows for the invoking user only, maybe?"""
    return 'Beep-boop'

async def async_gen():
    yield 'beep'
    yield 'boop'
    
@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def yield_async_gen(client, event):
    """Yields an async gen."""
    yield async_gen()

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def return_async_gen(client, event):
    """Returns an async gen."""
    return async_gen()


NEKO_LIFE = 'https://nekos.life/api/v2'

async def get_neko_life(client, keyword):
    yield
    url = f'{NEKO_LIFE}/{keyword}'
    
    async with client.http.get(url) as response:
        if response.status == 200:
            data = await response.json()
            content = data[keyword]
        else:
            content = 'Couldn\'t contact the API right now... OwO'
    
    yield content

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def text_cat(client, event):
    """I will send text cats :3"""
    return get_neko_life(client, 'cat')

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def why(client, event):
    """why are you using this commands?"""
    yield get_neko_life(client, 'why')


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def repeat(client, event,
        text : ('str', 'The content to repeat')
            ):
    """Repeats nya!"""
    if not text:
        text = 'nothing to repeat'
    
    return SlashResponse(text, allowed_mentions=None)


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def raffle(client, event,
        message : ('str', 'The message to raffle from'),
        emoji : ('str', 'The reactor users to raffle from.'),
            ):
    """Raffles an user out who reacted on a message."""
    guild = event.guild
    if (guild is None) or (guild not in client.guild_profiles):
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        abort('That\'s not an emoji.')
    
    message_reference = parse_message_reference(message)
    if message_reference is None:
        abort('Could not identify the message.')
    
    guild_id, channel_id, message_id = message_reference
    try:
        message = MESSAGES[message_id]
    except KeyError:
        if channel_id:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                abort('I have no access to the channel.')
                return
        else:
            channel = event.channel
        
        if not channel.cached_permissions_for(client).can_read_message_history:
            abort('I have no permission to get that message.')
        
        yield
        
        try:
            message = client.message_get(channel, message_id)
        except ConnectionError:
            # No internet
            return
        except DiscordException as err:
            if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                        ):
                # The message is already deleted.
                abort('The referenced message is already yeeted.')
                return
            
            if err.code == ERROR_CODES.invalid_access: # client removed
                # This is not nice.
                return
            
            if err.code == ERROR_CODES.invalid_permissions: # permissions changed meanwhile
                abort('I have no permission to get that message.')
                return
            
            raise
    
    yield
    
    users = await client.reaction_user_get_all(message)
    
    if users:
        user = choice(users)
        content = user.mention
    else:
        content = 'Could not find any user.'
    
    yield content
    return

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def loading(client, event):
    """Loading screen nya!"""
    if not client.is_owner(event.user):
        return 'Owner only.'
    
    await client.interaction_response_message_create(event)
    await sleep(0.5)
    await client.interaction_response_message_edit(event, content='loaded')

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def number(client, event, number:('number', 'number')):
    """Loading screen nya!"""
    return str(number)


async def async_gen_2():
    abort('beep')
    yield

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def abort_from_async_gen(client, event):
    """Aborts from an async gen."""
    return async_gen_2()

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def parse_time_delta(client, event,
        delta: (str, 'The delta to parse'),
            ):
    """Tries to parse a time delta."""
    delta = parse_tdelta(delta)
    if delta is None:
        result = 'Parsing failed.'
    else:
        result = repr(delta)
    
    return result

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def parse_relative_delta(client, event,
        delta: (str, 'The delta to parse'),
            ):
    """Tries to parse a relative delta."""
    delta = parse_rdelta(delta)
    if delta is None:
        result = 'Parsing failed.'
    else:
        result = repr(delta)
    
    return result

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def user_id(client, event,
        user_id: ('user_id', 'Get the id of an other user?', 'user') = None,
            ):
    """Shows your or the selected user's id."""
    if user_id is None:
        user_id = event.user.id
    
    return str(user_id)

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def collect_reactions(client, event):
    """Collects reactions"""
    message = yield SlashResponse('Collecting reactions for 1 minute!', force_new_message=True)
    await sleep(60.0)
    
    reactions = message.reactions
    if reactions:
        emojis = list(reactions)
        # Limit reactions to 16 to avoid error from Discord
        del emojis[16:]
        
        yield ' '.join(emoji.as_emoji for emoji in emojis)
    else:
        yield 'No reactions were collected.'

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__TESTER, True)
async def tester_only(client, event):
    """Tester only hopefully."""
    return 'Noice'

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__TESTER, True)
async def Late_abort(client, event):
    """Aborts after acknowledging."""
    yield
    abort('Nice?')


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def debug_command(client, event,
        command_name: (str, 'The command\'s name.')
            ):
    """Gets debug information about the given command."""
    if not client.is_owner(event.user):
        abort('Owner only.')
    
    if not command_name:
        abort('Empty command name.')
    
    application_commands = await client.application_command_guild_get_all(GUILD__NEKO_DUNGEON)
    for application_command in application_commands:
        if application_command.name == command_name:
            break
    else:
        abort('Command could not be found.')
    
    try:
        permission = await client.application_command_permission_get(GUILD__NEKO_DUNGEON, application_command)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_application_command_permissions:
            permission = None
        else:
            raise
    
    text_parts = [
        '**Application command**:\n'
        'Name : `', application_command.name, '`\n'
        'Id : `', repr(application_command.id), '`\n'
        'Allow by default : `', repr(application_command.allow_by_default), '`\n'
        '**Permission overwrites**:\n'
            ]
    
    if permission is None:
        overwrites = None
    else:
        overwrites = permission.overwrites
    
    if overwrites is None:
        text_parts.append('*none*')
    else:
        for index, overwrite in enumerate(overwrites):
            text_parts.append(repr(index))
            text_parts.append('.: type: `')
            text_parts.append(overwrite.type.name)
            text_parts.append('`; id: `')
            text_parts.append(repr(overwrite.target_id))
            
            target_name = overwrite.target.name
            if target_name:
                text_parts.append('`; name: `')
                text_parts.append(target_name)
            
            text_parts.append('`; allowed: `')
            text_parts.append(repr(overwrite.allow))
            text_parts.append('`\n')
    
    return ''.join(text_parts)

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ('user', 707113350785400884), True)
@set_permission(GUILD__NEKO_DUNGEON, ('user', 385575610006765579), True)
async def zeref_and_sleep_only(client, event):
    """Zeref and sleep only."""
    return 'LuL'

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
@set_permission(GUILD__NEKO_DUNGEON, ('user', 707113350785400884), False)
async def only_zeref_not(client, event):
    """Loli Police"""
    return 'Lets go nekos.'
