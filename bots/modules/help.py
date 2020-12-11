# -*- coding: utf-8 -*-
import sys

from hata import CLIENTS, USERS, GUILDS, CHANNELS, Embed, eventlist, Client, __version__
from hata.ext.commands import Command, checks, Converter, ConverterFlag, Closer
from bots.koishi import KOISHI_HELP_COLOR, DUNGEON_INVITE, DUNGEON, WORSHIPPER_ROLE, EVERYNYAN_ROLE, \
    ANNOUNCEMNETS_ROLE, WELCOME_CHANNEL

from bot_utils.shared import KOISHI_GIT, HATA_GIT, DUNGEON_INVITE, DUNGEON, HATA_DOCS, TORTOISE_PASTE

HELP_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(HELP_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(HELP_COMMANDS)

@HELP_COMMANDS.from_class
class about:
    async def command(client, message):
        implement = sys.implementation
        embed = Embed('About', f'Hello, I am {client.full_name} as you expected. What did you think, who am I?',
                color=KOISHI_HELP_COLOR) \
            .add_field('Library', f'[hata {__version__}]({HATA_GIT})', inline=True) \
            .add_field('Interpreter', (
                f'Python{implement.version[0]}.{implement.version[1]}'
                f'{"" if implement.version[3]=="final" else " "+implement.version[3]} {implement.name}'
                    ), inline=True) \
            .add_field('Support server', f'[{DUNGEON.name}]({DUNGEON_INVITE.url})', inline=True) \
            .add_field('Clients', repr(len(CLIENTS)), inline=True) \
            .add_field('Guilds', repr(len(GUILDS)), inline=True) \
            .add_field('Users', repr(len(USERS)), inline=True) \
            .add_thumbnail(client.application.icon_url_as(size=128))
        
        await client.message_create(message.channel, embed=embed)
    
    category = 'HELP'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('about', (
            'Just some information about me.'
            f'Usage: `{prefix}about`'
                ), color=KOISHI_HELP_COLOR)

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
async def aliases(client, message, name:str, target_client: Converter('client', flags=ConverterFlag.client_all, default_code='client')):
    while True:
        if len(name) > 64:
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
    
    await client.message_create(message.channel, embed=Embed(title, description, color=KOISHI_HELP_COLOR))
    
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
            ).add_field(
                'Alternative accounts',
                'Instant ban.'
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


@HELP_COMMANDS(category='HELP', aliases=['hata_docs'],)
async def docs(client, message):
    """
    Sends a link to hata's documentation.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[hata docs]({HATA_DOCS})', color=KOISHI_HELP_COLOR))


@HELP_COMMANDS(category='HELP', aliases=['how-to-ask'])
async def ask(client, message):
    """
    How to ask!
    """
    embed = Embed('How to ask?',
        'Don\'t ask to ask just ask.\n'
        '\n'
        ' • You will have much higher chances of getting an answer\n'
        ' • It saves time both for us and you as we can skip the whole process of actually getting the question '
        'out of you\n'
        '\n'
        'For more info visit [dontasktoask.com](https://dontasktoask.com/)',
            color = KOISHI_HELP_COLOR)
    
    await Closer(client, message.channel, embed)


@HELP_COMMANDS(category='HELP')
async def markdown(client, message):
    """
    How to use markdown.
    """
    embed = Embed('Markdown',
        'You can format your code by using markdown like this:\n'
        '\n'
        '\\`\\`\\`py\n'
        'print(\'Hello world\')\n'
        '\\`\\`\\`\n'
        '\n'
        'This would give you:\n'
        '```python\n'
        'print(\'Hello world\')```\n'
        'Note that character ` is not a quote but a backtick.\n'
        '\n'
        f'If, however, you have large amounts of code then it\'s better to use [our paste service]({TORTOISE_PASTE}).',
            color = KOISHI_HELP_COLOR)
    
    await Closer(client, message.channel, embed)


@HELP_COMMANDS(category='HELP')
async def paste(client, message):
    """
    A link to our paste service.
    """
    embed = Embed(description=f'[Paste link]({TORTOISE_PASTE})', color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel, embed=embed)
