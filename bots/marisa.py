# -*- coding: utf-8 -*-
import sys
from random import random

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

@Marisa.interactions(guild=DUNGEON, name='guild-icon')
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
    """Shows the given emoji"""
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
        user : ('user', 'To who?'),
            ):
    """Gifts a cookie!"""
    return Embed(description=f'{event.user:f} just gifted a cookie to {user:f}')


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

@Marisa.interactions(guild=DUNGEON, show_source=False, name='do-things')
async def do_things(client, event):
    """I will do things!"""
    yield '*Doing things*'
    await sleep(1.0+random()*4.0, KOKORO)
    yield choose(DO_THINGS_CHOICES)


@Marisa.interactions(guild=DUNGEON, show_source=False)
async def perms(client, event):
    """Showing your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        description = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        description = '*none*'
    
    user = event.user
    return Embed('Permissions', description).add_author(user.avatar_url, user.full_name)
