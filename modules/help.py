# -*- coding: utf-8 -*-
import sys

from hata import CLIENTS, USERS, GUILDS, CHANNELS, Embed, eventlist, Client
from hata.ext.commands import Command, checks, Converter, ConverterFlag, Closer
from koishi import KOISHI_HELP_COLOR, DUNGEON_INVITE, DUNGEON, WORSHIPPER_ROLE, EVERYNYAN_ROLE, ANNOUNCEMNETS_ROLE, \
    WELCOME_CHANNEL

KOISHI_GIT = 'https://github.com/HuyaneMatsu/Koishi'
HATA_GIT = 'https://github.com/HuyaneMatsu/hata'

HELP_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(HELP_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(HELP_COMMANDS)

@HELP_COMMANDS.from_class
class about:
    async def command(client, message):
        implement = sys.implementation
        embed = Embed('About',(
            f'Me, {client.full_name}, I am general purpose/test client.'
            '\n'
            'My code base is'
            f' [open source]({KOISHI_GIT}). '
            'One of the main goal of my existence is to test the best *cough*'
            f' [discord API wrapper]({HATA_GIT}). '
            '\n\n'
            f'My Masutaa is {client.owner.full_name} (send neko pictures pls).\n\n'
            '**Client info**\n'
            f'Python version: {implement.version[0]}.{implement.version[1]}'
            f'{"" if implement.version[3]=="final" else " "+implement.version[3]}\n'
            f'Interpreter: {implement.name}\n'
            f'Clients: {len(CLIENTS)}\n'
            f'Users: {len(USERS)}\n'
            f'Guilds: {len(GUILDS)}\n'
            f'Channels: {len(CHANNELS)}\n'
            'Power level: over 9000!\n'
                )).add_thumbnail(client.application.icon_url_as(size=128))
        
        await client.message_create(message.channel,embed=embed)
    
    category = 'HELP'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('about',(
            'Just some information about me.'
            f'Usage: `{prefix}about`'
                ),color=KOISHI_HELP_COLOR)

@HELP_COMMANDS.from_class
class invite:
    async def command(client, message):
        await client.message_create(message.channel, DUNGEON_INVITE.url)
    
    category = 'HELP'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('invite',(
            f'Sends an invite to our {DUNGEON} guild.\n'
            f'Usage : `{prefix}invite`'
                ),color=KOISHI_HELP_COLOR)


async def aliases_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('aliases',(
        'Do you wanna know one of my command\'s aliases?\n'
        f'Type `{prefix}aliases <name>` and check them out!\n\n'
        'Or if you wanna know someone elses, who I might spy on, type her name after the command\'s :3.'
            ), color=KOISHI_HELP_COLOR)


async def aliases_parser_failure_handler(client, message, command, content, args):
    await Closer(client, message.channel, aliases_description(client, message))

@HELP_COMMANDS(description=aliases_description, category='HELP', parser_failure_handler=aliases_parser_failure_handler)
async def aliases(client, message, name:str, target_client:Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default=None)):
    if type(target_client) is not Client:
        target_client = client
    
    while True:
        if len(name)>64:
            fail = True
            break
        
        if not name.islower():
            name = name.lower()
        
        try:
            command = target_client.command_processer.commands[name]
        except KeyError:
            fail = True
            break
        
        if await command.run_all_checks(target_client, message):
            fail = False
            break
            
        fail = True
        break
    
    if fail:
        title = None
        if client is target_client:
            description = f'I have no command named as {name!r}.'
        else:
            description = f'{target_client.name_at(message.guild)} has no command named as {name!r}.'
    else:
        aliases = command.aliases
        if aliases is None:
            title = f'There are no alises provided for command: {name!r}.'
            description = None
        else:
            title = f'Aliases for: {command.display_name!r}:'
            description = '\n'.join(aliases)
    
    await client.message_create(message.channel,embed=Embed(title,description,color=KOISHI_HELP_COLOR))
    
@HELP_COMMANDS.from_class
class rules:
    async def command(client, message):
        embed = Embed(f'Rules of {DUNGEON}:', color = KOISHI_HELP_COLOR,
            ).add_field(
                'Guidelines',
                'Follow [Discord\'s guidelines](https://discord.com/guidelines)',
            ).add_field(
                'Behaviour',
                'Listen to staff and follow their instructions.',
            ).add_field(
                'Language',
                f'{DUNGEON} is an english speaking server, please try to stick yourself to it.',
            ).add_field(
                'Channels',
                'Read the channel\'s topics. Make sure to keep the conversations in their respective channels.'
            ).add_field(
                'Usernames',
                'Invisible, offensive or noise unicode names are not allowed.'
            ).add_field(
                'Spamming',
                'Forbidden in any form. Spamming server members in DM-s counts as well.',
            ).add_field(
                'NSFW',
                'Keep explicit content in nsfw channels',
            ).add_field(
                'Roles',
                f'Do not beg for roles. You can claim {EVERYNYAN_ROLE.mention} role, what gives you access to '
                f'additional channels by typing `nya` at {WELCOME_CHANNEL.mention}.\n'
                f'*You must be the member of the guild for at least 10 minutes and {client.mention} must be online '
                f'as well.*'
                '\n\n'
                f'Addtionally you can also claim (or unclaim) {ANNOUNCEMNETS_ROLE.mention} by typing `i meow` '
                '(or `i not meow`), or if you are the member of the server for at least half year, you can claim the '
                f'superior {WORSHIPPER_ROLE.mention} role by typing `nekogirl`!'
            ).add_field(
                'Advertisements',
                'Advertising other social medias, servers, communities or services in chat or in DM-s are disallowed.'
            ).add_field(
                'No political or religious topics.',
                'I do not say either that aliens exists, even tho they do.',
            )
        await client.message_create(message.channel, embed=embed, allowed_mentions=None)
        
        if message.channel.cached_permissions_for(client).can_manage_messages:
            await client.message_delete(message)
        
    category = 'HELP'
    checks = [checks.owner_only(), checks.is_guild(DUNGEON)]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('rules',(
            f'Shows the rules of the {DUNGEON} guild.'
            f'Usage : `{prefix}rules`'
                ),color=KOISHI_HELP_COLOR).add_footer(
                f'Owner only and can be used only at {DUNGEON}.')


@HELP_COMMANDS(category='HELP')
async def git(client, message):
    """
    Sends a link to my git repository.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[Koishi repository]({KOISHI_GIT})', color=KOISHI_HELP_COLOR))


@HELP_COMMANDS(category='HELP', aliases=['wrapper'])
async def hata(client, message):
    """
    Sends a link to my wrapper's git repository.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[hata repository]({HATA_GIT})', color=KOISHI_HELP_COLOR))

