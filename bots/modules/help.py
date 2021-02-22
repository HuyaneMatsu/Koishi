# -*- coding: utf-8 -*-
import sys

from hata import CLIENTS, USERS, GUILDS, Embed, Client, __version__
from hata.ext.commands import checks, Closer

from bot_utils.shared import LINK__KOISHI_GIT, LINK__HATA_GIT, INVITE__NEKO_DUNGEON, GUILD__NEKO_DUNGEON, \
    LINK__HATA_DOCS, LINK__PASTE, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, COLOR__KOISHI_HELP, ROLE__NEKO_DUNGEON__ELEVATED, \
    ROLE__NEKO_DUNGEON__VERIFIED, CHANNEL__NEKO_DUNGEON__SYSTEM
from bot_utils.command_utils import CLIENT_CONVERTER_ALL_CLIENT_DEFAULT

Koishi: Client
@Koishi.commands.from_class
class about:
    async def command(client, message):
        implement = sys.implementation
        embed = Embed('About', f'Hello, I am {client.full_name} as you expected. What did you think, who am I?',
                color=COLOR__KOISHI_HELP) \
            .add_field('Library', f'[hata {__version__}]({LINK__HATA_GIT})', inline=True) \
            .add_field('Interpreter', (
                f'Python{implement.version[0]}.{implement.version[1]}'
                f'{"" if implement.version[3]=="final" else " "+implement.version[3]} {implement.name}'
                    ), inline=True) \
            .add_field('Support server', f'[{GUILD__NEKO_DUNGEON.name}]({INVITE__NEKO_DUNGEON.url})', inline=True) \
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
                ), color=COLOR__KOISHI_HELP)

@Koishi.commands.from_class
class invite:
    async def command(client, message):
        await client.message_create(message.channel, INVITE__NEKO_DUNGEON.url)
    
    category = 'HELP'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('invite',(
            f'Sends an invite to our {GUILD__NEKO_DUNGEON} guild.\n'
            f'Usage : `{prefix}invite`'
                ),color=COLOR__KOISHI_HELP)


async def aliases_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('aliases',(
        'Do you wanna know one of my command\'s aliases?\n'
        f'Type `{prefix}aliases <name>` and check them out!\n\n'
        'Or if you wanna know someone else\'s, who I might spy on, type her name after the command\'s :3.'
            ), color=COLOR__KOISHI_HELP)


async def aliases_parser_failure_handler(client, message, command, content, args):
    embed = await aliases_description(client, message)
    await Closer(client, message.channel, embed)

@Koishi.commands(
    description = aliases_description,
    category = 'HELP',
    parser_failure_handler = aliases_parser_failure_handler,
        )
async def aliases(client, message, name:str, target_client: CLIENT_CONVERTER_ALL_CLIENT_DEFAULT):
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
            title = f'There are no aliases provided for command: {name!r}.'
            description = None
        else:
            title = f'Aliases for: {command.display_name!r}:'
            description = '\n'.join(aliases)
    
    await client.message_create(message.channel, embed=Embed(title, description, color=COLOR__KOISHI_HELP))
    
@Koishi.commands.from_class
class rules:
    async def command(client, message):
        embed = Embed(f'Rules of {GUILD__NEKO_DUNGEON}:', color = COLOR__KOISHI_HELP,
            ).add_field(
                'Guidelines',
                'Follow [Discord\'s guidelines](https://discord.com/guidelines)',
            ).add_field(
                'Behaviour',
                'Listen to staff and follow their instructions.',
            ).add_field(
                'Language',
                f'{GUILD__NEKO_DUNGEON} is an english speaking server, please try to stick yourself to it.',
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
                'Keep explicit content in nsfw channels.',
            ).add_field(
                'Roles',
                f'Do not beg for roles. You can claim {ROLE__NEKO_DUNGEON__VERIFIED.mention} role, what gives you access to '
                f'additional channels by typing `nya` at {CHANNEL__NEKO_DUNGEON__SYSTEM.mention}.\n'
                f'*You must be the member of the guild for at least 10 minutes and {client.mention} must be online '
                f'as well.*'
                '\n\n'
                f'Additionally you can also claim (or un-claim) {ROLE__NEKO_DUNGEON__ANNOUNCEMENTS.mention} by typing '
                f'`i meow` (or `i not meow`), or if you are the member of the server for at least half year, you can '
                f'claim the superior {ROLE__NEKO_DUNGEON__ELEVATED.mention} role by typing `nekogirl`!'
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
    checks = [checks.owner_only(), checks.is_guild(GUILD__NEKO_DUNGEON)]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('rules',(
            f'Shows the rules of the {GUILD__NEKO_DUNGEON} guild.'
            f'Usage : `{prefix}rules`'
                ),color=COLOR__KOISHI_HELP).add_footer(
                f'Owner only and can be used only at {GUILD__NEKO_DUNGEON}.')


@Koishi.commands(category='HELP', aliases='github')
async def git(client, message):
    """
    Sends a link to my git repository.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[Koishi repository]({LINK__KOISHI_GIT})', color=COLOR__KOISHI_HELP))


@Koishi.commands(category='HELP', aliases='wrapper')
async def hata(client, message):
    """
    Sends a link to my wrapper's git repository.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[hata repository]({LINK__HATA_GIT})', color=COLOR__KOISHI_HELP))


@Koishi.commands(category='HELP', aliases='hata-docs',)
async def docs(client, message):
    """
    Sends a link to hata's documentation.
    """
    await client.message_create(message.channel, embed= \
        Embed(description=f'[hata docs]({LINK__HATA_DOCS})', color=COLOR__KOISHI_HELP))


@Koishi.commands(category='HELP', aliases='how-to-ask')
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
            color = COLOR__KOISHI_HELP)
    
    await Closer(client, message.channel, embed)


@Koishi.commands(category='HELP')
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
        'Note that character \` is not a quote but a backtick.\n'
        '\n'
        f'If, however, you have large amounts of code then it\'s better to use [our paste service]({LINK__PASTE}).',
            color = COLOR__KOISHI_HELP)
    
    await Closer(client, message.channel, embed)


@Koishi.commands(category='HELP')
async def paste(client, message):
    """
    A link to our paste service.
    """
    embed = Embed(description=f'[Paste link]({LINK__PASTE})', color=COLOR__KOISHI_HELP)
    await client.message_create(message.channel, embed=embed)
