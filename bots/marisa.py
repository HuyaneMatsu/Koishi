# -*- coding: utf-8 -*-
import sys
from random import random, choice
from time import perf_counter

from bs4 import BeautifulSoup

from hata import Embed, Client, parse_emoji, DATETIME_FORMAT_CODE, elapsed_time, id_to_time, sleep, KOKORO
from hata.ext.commands import setup_ext_commands, checks
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import setup_ext_slash

from bot_utils.shared import category_name_rule, DEFAULT_CATEGORY_NAME, MARISA_PREFIX, MARISA_HELP_COLOR, \
    command_error, DUNGEON
from bot_utils.syncer import sync_request_comamnd
from bot_utils.interpreter import Interpreter
from bot_utils.tools import choose

Marisa : Client

setup_ext_commands(Marisa, MARISA_PREFIX, default_category_name=DEFAULT_CATEGORY_NAME,
    category_name_rule=category_name_rule)

setup_ext_slash(Marisa, immediate_sync=True)

Marisa.command_processer.create_category('TEST COMMANDS', checks=checks.owner_only())
Marisa.command_processer.create_category('VOICE', checks=checks.guild_only())

Marisa.commands(SubterraneanHelpCommand(MARISA_HELP_COLOR), 'help', category='HELP')

Marisa.commands(command_error, checks=[checks.is_guild(DUNGEON)])

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
            ), color=MARISA_HELP_COLOR).add_footer(
            'Owner only!')

Marisa.commands(Interpreter(locals().copy()), name='execute', description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])

Marisa.commands(sync_request_comamnd, name='sync', category='UTILITY', checks=[checks.owner_only()])


@Marisa.interactions(guild=DUNGEON)
async def avatar(client, event,
        user : ('user', 'Choose a user!') = None,
            ):
    """Shows your or the chosen user's avatar."""
    if user is None:
        user = event.user
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    return Embed(f'{user:f}\'s avatar', color=color, url=url).add_image(url)

@Marisa.interactions(guild=DUNGEON)
async def guild_icon(client, event,
        choice: ({
            'Icon'             : 'icon'             ,
            'Banner'           : 'banner'           ,
            'Discovery-splash' : 'discovery_splash' ,
            'Invite-splash'    : 'invite_splash'    ,
                }, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon."""
    guild = event.guild
    if (guild is None) or guild.partial:
        return Embed('Error', 'The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size=4096)
        hash_value = guild.icon_hash
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size=4096)
        hash_value = guild.banner_hash
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size=4096)
        hash_value = guild.discovery_splash_hash
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size=4096)
        hash_value = guild.invite_splash_hash
    
    if url is None:
        color = (event.id>>22)&0xFFFFFF
        return Embed(f'{guild.name} has no {name}', color=color)
    
    color = hash_value&0xFFFFFF
    return Embed(f'{guild.name}\'s {name}', color=color, url=url).add_image(url)

@Marisa.interactions(guild=DUNGEON)
async def showemoji(client, event,
        emoji : ('str', 'Yes?'),
            ):
    """Shows the given emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'


@Marisa.interactions(guild=DUNGEON, name='id-to-time')
async def idtotime(client, event,
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'


@Marisa.interactions(guild=DUNGEON, show_source=False)
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

@Marisa.interactions(guild=DUNGEON, show_source=False)
async def do_things(client, event):
    """I will do things!"""
    yield '*Doing things*'
    await sleep(1.0+random()*4.0, KOKORO)
    yield choose(DO_THINGS_CHOICES)


@Marisa.interactions(guild=DUNGEON, show_source=False)
async def perms(client, event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        description = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        description = '*none*'
    
    user = event.user
    return Embed('Permissions', description).add_author(user.avatar_url, user.full_name)


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


@Marisa.interactions(guild=DUNGEON)
async def roll(client, event,
        dice_count: ([(str(v), v) for v in range(1, 7)], 'With how much dice do you wanna roll?') = 1,
            ):
    """Rolls with dices."""
    return str(round((1.+(random()*5.))*dice_count))

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


SCARLET = Marisa.interactions(None, name='scarlet', description='Scarlet?', guild=DUNGEON)

@SCARLET.interactions
async def flandre(client, event):
    """Flandre!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'flandre_scarlet', 'Scarlet Flandre', 0xdc143c)


@SCARLET.interactions
async def remilia(client, event):
    """Remilia!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'remilia_scarlet', 'Remilia Flandre', 0x9400d3)


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
        guild = DUNGEON,
        show_source = False,
            )

# Cleanup
del action_name, embed_color


@Marisa.interactions(guild=DUNGEON)
async def repeat(client, event,
        text: ('str', 'Uhum?')
            ):
    """What should I exactly repeat?"""
    await client.interaction_response_message_create(event, text, allowed_mentions=None, show_source=True)

@Marisa.interactions(guild=DUNGEON)
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

@Marisa.interactions(guild=DUNGEON)
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
