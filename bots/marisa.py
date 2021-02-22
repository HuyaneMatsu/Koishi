# -*- coding: utf-8 -*-
import sys
from random import random, choice, shuffle
from time import perf_counter
from math import ceil
from collections import deque
from html import unescape as html_unescape
from functools import partial as partial_func

from bs4 import BeautifulSoup
from dateparser import parse as parse_date

from hata import Embed, Client, parse_emoji, DATETIME_FORMAT_CODE, elapsed_time, id_to_time, sleep, KOKORO, cchunkify, \
    alchemy_incendiary, RoleManagerType, ICON_TYPE_NONE, BUILTIN_EMOJIS, Status, ChannelText, ChannelVoice, Lock, \
    ChannelCategory, ChannelStore, ChannelThread, time_to_id
from hata.ext.commands import setup_ext_commands, checks, Pagination, wait_for_reaction
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import setup_ext_slash
from hata.backend.futures import render_exc_to_list

from bot_utils.shared import category_name_rule, DEFAULT_CATEGORY_NAME, PREFIX__MARISA, COLOR__MARISA_HELP, \
    command_error, GUILD__NEKO_DUNGEON, CHANNEL__NEKO_DUNGEON__DEFAULT_TEST
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

@Marisa.events
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

@Marisa.events(overwrite=True)
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
        
        # Request image information
        async with client.http.get(SAFE_BOORU+tags) as response:
            if response.status != 200:
                return Embed('Error', 'Safe-booru unavailable', color=color)
            
            result = await response.read()
        
        # Read response and get image urls.
        soup = BeautifulSoup(result, 'lxml')
        image_urls = [post['file_url'] for post in soup.find_all('post')]
        
        if not image_urls:
            return Embed('Error', 'No images found.\nPlease try again later.', color=color)
        
        # If we received image urls, cache them
        IMAGE_URL_CACHE[tags] = image_urls
    
    image_url = choice(image_urls)
    return Embed(name, color=color, url=image_url).add_image(image_url)


SCARLET = Marisa.interactions(None, name='scarlet', description='Scarlet?', guild=GUILD__NEKO_DUNGEON)

@SCARLET.interactions
async def flandre(client, event):
    """Flandre!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'flandre_scarlet', 'Scarlet Flandre', 0xdc143c)

@SCARLET.interactions
async def remilia(client, event):
    """Remilia!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'remilia_scarlet', 'Scarlet Remilia', 0x9400d3)

@SCARLET.interactions(is_default=True)
async def devil(client, event):
    """Flandre & Remilia!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'flandre_scarlet+remilia_scarlet', 'Scarlet Flandre & Remilia', 0xa12a2a)

class Action(object):
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


@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def repeat(client, event,
        text: ('str', 'Uhum?')
            ):
    """What should I exactly repeat?"""
    await client.interaction_response_message_create(event, text, allowed_mentions=None)

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

def match_message_author(user, message):
    return (message.author is user)

@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def clear(client, event,
        limit : ('int'      , 'How much message?'                        )        ,
        before : ('str'     , 'Till when?'                               ) = None ,
        after  : ('str'     , 'Since when?'                              ) = None ,
        where  : ('channel' , 'Where?'                                   ) = None ,
        whos   : ('user'    , 'Who\'s message?'                          ) = None ,
        reason : ('str'     , 'Will show up in the guild\'s audit logs.' ) = None ,
            ):
    """Yeets messages."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    if where is None:
        channel = event.channel
    else:
        if not isinstance(where, ChannelText):
            yield Embed('Error', 'The channel must be a text channel.')
            return
        
        channel = where
    
    if limit < 1:
        yield Embed('Ohoho', '`limit` cannot be non-positive.')
        return
    
    if not event.user_permissions.can_administrator:
        yield Embed('Permission denied', 'You must have administrator permission to use this command.')
        return
    
    client_permissions = channel.cached_permissions_for(client)
    if (not client_permissions.can_manage_messages) or (not client_permissions.can_read_message_history):
        yield Embed('Permission denied',
            'I must have manage messages and read message history in the channel to do it.')
        return
    
    if (before is None) or (not before):
        before = event.id
    else:
        try:
            date = parse_date(before)
        except ValueError:
            yield Embed('Error', '`before` could not be parsed.')
            return
        
        before = time_to_id(date)
    
    if (after is None) or (not after):
        after = 0
    else:
        try:
            date = parse_date(after)
        except ValueError:
            yield Embed('Error', '`after` could not be parsed.')
            return
        
        after = time_to_id(date)
    
    yield
    
    if whos is None:
        filter = None
    else:
        filter = partial_func(match_message_author, whos)
    
    if (reason is not None) and (not reason):
        reason = None
    
    await client.multi_client_message_delete_sequence(channel, after=after, before=before, limit=limit, filter=filter,
        reason=reason)


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
