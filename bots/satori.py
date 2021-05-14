# -*- coding: utf-8 -*-
import signal
from random import randint
from itertools import cycle, chain
from threading import main_thread

from hata import DiscordException, Embed, ERROR_CODES, BUILTIN_EMOJIS, Emoji, WebhookType, KOKORO, Client, CLIENTS, \
    Permission
from hata.ext.commands import setup_ext_commands, checks, Closer
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import setup_ext_slash

from bot_utils.shared import PREFIX__SATORI, COLOR__SATORI_HELP, category_name_rule, DEFAULT_CATEGORY_NAME
from bot_utils.tools import MessageDeleteWaitfor, MessageEditWaitfor
from bot_utils.interpreter import Interpreter

Satori : Client

Satori.events(MessageDeleteWaitfor)
Satori.events(MessageEditWaitfor)

setup_ext_commands(Satori, PREFIX__SATORI, default_category_name=DEFAULT_CATEGORY_NAME,
    category_name_rule=category_name_rule)
setup_ext_slash(Satori)

Satori.commands(SubterraneanHelpCommand(COLOR__SATORI_HELP), 'help')

@Satori.commands
async def invalid_command(client, message, command, content):
    guild = message.guild
    if guild is None:
        try:
            await client.message_create(message.channel,
                'Eeh, what should I do, what should I do?!?!')
        except BaseException as err:
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.cannot_send_message_to_user, # dm disabled
                            ):
                    return
            
            await client.events.error(client, 'invalid_command', err)
            return
        return
    
    await client.message_create(message.channel, 'I have no idea, hmpff...')

TRANSFORMATIONS = {
    ' ': ' ',
    '#': BUILTIN_EMOJIS['hash'].as_emoji,
    '*': BUILTIN_EMOJIS['asterisk'].as_emoji,
    '0': BUILTIN_EMOJIS['zero'].as_emoji,
    '1': BUILTIN_EMOJIS['one'].as_emoji,
    '2': BUILTIN_EMOJIS['two'].as_emoji,
    '3': BUILTIN_EMOJIS['three'].as_emoji,
    '4': BUILTIN_EMOJIS['four'].as_emoji,
    '5': BUILTIN_EMOJIS['five'].as_emoji,
    '6': BUILTIN_EMOJIS['six'].as_emoji,
    '7': BUILTIN_EMOJIS['seven'].as_emoji,
    '8': BUILTIN_EMOJIS['eight'].as_emoji,
    '9': BUILTIN_EMOJIS['nine'].as_emoji,
        }
    
for char in range(b'a'[0], b'z'[0]+1):
    emoji = BUILTIN_EMOJIS['regional_indicator_'+chr(char)].as_emoji
    TRANSFORMATIONS[chr(char)] = emoji
    TRANSFORMATIONS[chr(char-32)] = emoji

del char, emoji

@Satori.commands
async def emojify(client, message, content):
    if not content:
        return
    
    if len(content) > 80:
        await client.message_create(message.channel, 'Message too long')
        return
    
    result = []
    for char in content:
        try:
            emoji = TRANSFORMATIONS[char]
        except KeyError:
            pass
        else:
            result.append(emoji)

        continue
    
    result = '\u200b'.join(result)
    # If the message is empty, we will check that anyways
    await client.message_create(message, result, allowed_mentions=None)
    return

@Satori.commands.from_class
class auto_pyramid:
    async def command(client, message, emoji:Emoji, size:int):
        while True:
            if size < 2:
                error_message = 'That is pretty small. OOF'
            elif size > 23:
                error_message = 'That is HUGE! That\'s what she said...'
            else:
                break
            
            await client.message_create(message.channel, error_message)
            return
        
        should_check_external = (emoji.is_custom_emoji() and (emoji.guild is not message.guild))
        
        available_clients = []
        
        channel = message.channel
        for client_ in channel.clients:
            permissions = channel.cached_permissions_for(client_)
            if not permissions.can_send_messages:
                continue
            
            if not client_.can_use_emoji(emoji):
                continue
            
            if should_check_external and (not permissions.can_use_external_emojis):
                continue
            
            available_clients.append(client_)
        
        if len(available_clients) < 2:
            await client.message_create(message.channel,f'There need to be at least 2 client at the channel, who can '
                f'build a pyramid, meanwhile there is only {len(available_clients)}')
            return
        
        
        for client_, count in zip(cycle(available_clients), chain(range(1,size),range(size,0,-1))):
            await client_.message_create(channel, ' '.join(emoji.as_emoji for _ in range(count)))
    
    checks = [checks.has_guild_permissions(Permission().update_by_keys(manage_messages=True))]
    
    async def description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('auto-pyramid', (
            'Creates a pyramid!\n'
            f'Usage: `{prefix}auto-pyramid <emoji> <size>`'
                ), color=COLOR__SATORI_HELP).add_footer(
                'Guild only! You must have manage messages permission to use it.')
    
    async def parser_failure_handler(client, message, command, content, args):
        embed = await command.description(client, message)
        await Closer(client, message.channel, embed)

@Satori.commands.from_class
class auto_pyramid_u:
    async def command(client, message, emoji:Emoji, size:int):
        while True:
            if size < 2:
                error_message = 'That is pretty small. OOF'
            elif size > 23:
                error_message = 'That is HUGE! That\'s what she said...'
            else:
                break
            
            await client.message_create(message.channel, error_message)
            return
        
        if emoji.is_custom_emoji() and (emoji.managed or (emoji.roles is not None) or (emoji.guild is not message.guild)):
            await client.message_create(message.channel, 'No managed, limited to role or outer custom emojis are allowed.')
            return
        
        channel = message.channel
        if not channel.cached_permissions_for(client).can_manage_webhooks:
            await client.message_create(channel, 'I need manage webhooks permission to execute this command.')
            return
        
        webhooks = await client.webhook_get_all_channel(channel)
        for webhook in webhooks:
            if webhook.type is WebhookType.bot:
                executor_webhook = webhook
                break
        else:
            executor_webhook = None
        
        if (executor_webhook is None):
            executor_webhook = await client.webhook_create(channel, 'auto-pyramider')
        
        users = list(message.guild.users.values())
        selected_users = []
        needed_users = (size<<1) - 1
        user_count = len(users)
        while True:
            if user_count == 0:
                break
            
            if needed_users == 0:
                break
            
            user = users.pop(randint(0, user_count-1))
            user_count -= 1
            if user.is_bot:
                continue
            
            selected_users.append(user)
            needed_users -= 1
        
        if needed_users:
            await client.message_create(channel, 'The guild does not have enough users for this size of pyramid.')
            return
        
        for user, count in zip(selected_users, chain(range(1, size), range(size, 0, -1))):
            await client.webhook_message_create(executor_webhook, ' '.join(emoji.as_emoji for _ in range(count)),
                name=user.name_at(message.guild), avatar_url=user.avatar_url_as(size=4096), wait=True)
    
    checks = [checks.has_guild_permissions(Permission().update_by_keys(manage_messages=True))]
    
    async def description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('auto-pyramid-u', (
            'Creates a pyramid!\n'
            f'Usage: `{prefix}auto-pyramid-u <emoji> <size>`'
                ), color=COLOR__SATORI_HELP).add_footer(
                'Guild only! You must have manage messages permission to use it.')
    
    async def parser_failure_handler(client, message, command, content, args):
        embed = await command.description(client, message)
        await Closer(client, message.channel, embed)

@Satori.commands.from_class
class reverse:
    async def command(client, message, content):
        if content:
            await client.message_create(message, content[::-1], allowed_mentions=None)
    
    async def description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('reverse', (
            'Reverses your message\n'
            f'Usage: `{prefix}reverse <content>`'
                ), color=COLOR__SATORI_HELP)


@Satori.commands.from_class
class shutdown:
    async def command(client, message):
        
        for client_ in CLIENTS.values():
            await client_.disconnect()
        
        await client.message_create(message.channel, 'Clients stopped, stopping process.')
        KOKORO.stop()
        thread_id = main_thread().ident
        signal.pthread_kill(thread_id, signal.SIGKILL)
    
    category = 'UTILITY'
    checks = checks.owner_only()
    
    async def description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('shutdown', (
            'Shuts the clients down, then stops the process.'
            f'Usage  `{prefix}shutdown`'
            ), color=COLOR__SATORI_HELP).add_footer(
                'Owner only!')

async def execute_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
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
            ), color=COLOR__SATORI_HELP).add_footer(
            'Owner only!')

Satori.commands(Interpreter(locals().copy()), name='execute', description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])
