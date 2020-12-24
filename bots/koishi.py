# -*- coding: utf-8 -*-
import re, signal
from datetime import datetime, timedelta
from threading import main_thread

from hata import BUILTIN_EMOJIS, Embed, sleep, CLIENTS,  Client, KOKORO
from hata.ext.commands import checks, setup_ext_commands
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand

from bot_utils.tools import MessageDeleteWaitfor, GuildDeleteWaitfor, RoleDeleteWaitfor, ChannelDeleteWaitfor, \
    EmojiDeleteWaitfor, RoleEditWaitfor
from bot_utils.shared import KOISHI_PREFIX, category_name_rule, DEFAULT_CATEGORY_NAME, WELCOME_CHANNEL, DUNGEON, \
    ANNOUNCEMNETS_ROLE, WORSHIPPER_ROLE, KOISHI_HELP_COLOR, SYNC_CHANNEL, command_error, EVERYNYAN_ROLE

from bot_utils.interpreter import Interpreter
from bot_utils.syncer import sync_request_waiter

_KOISHI_NOU_RP = re.compile(r'n+\s*o+\s*u+', re.I)
_KOISHI_OWO_RP = re.compile('(owo|uwu|0w0)', re.I)
_KOISHI_OMAE_RP = re.compile('omae wa mou', re.I)

Koishi: Client

setup_ext_commands(Koishi, KOISHI_PREFIX, default_category_name=DEFAULT_CATEGORY_NAME,
    category_name_rule=category_name_rule)

Koishi.command_processer.append(SYNC_CHANNEL, sync_request_waiter)

Koishi.events(MessageDeleteWaitfor)
Koishi.events(GuildDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(ChannelDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleEditWaitfor)

Koishi.commands(SubterraneanHelpCommand(KOISHI_HELP_COLOR), 'help', category='HELP')

Koishi.command_processer.create_category('ADMINISTRATION',)
Koishi.command_processer.create_category('GAMES',)
Koishi.command_processer.create_category('UTILITY',)
Koishi.command_processer.create_category('VOICE', checks=checks.guild_only())

@Koishi.commands
async def default_event(client, message):
    if (message.referenced_message is not None):
        return
    
    user_mentions = message.user_mentions
    if  (user_mentions is not None) and (client in user_mentions):
        author = message.author
        m1 = author.mention
        m2 = client.mention
        m3 = author.mention_nick
        m4 = client.mention_nick
        replace = {
            '@everyone'   : '@\u200beveryone',
            '@here'       : '@\u200bhere',
            re.escape(m1) : m2,
            re.escape(m2) : m1,
            re.escape(m3) : m4,
            re.escape(m4) : m3,
                }
        pattern = re.compile('|'.join(replace.keys()))
        result = pattern.sub(lambda x: replace[re.escape(x.group(0))], message.content)
        await client.message_create(message.channel, result, allowed_mentions=[author])
        return
        
    content = message.content
    if message.channel.cached_permissions_for(client).can_add_reactions and (_KOISHI_NOU_RP.match(content) is not None):
        for value in 'nou':
            emoji = BUILTIN_EMOJIS[f'regional_indicator_{value}']
            await client.reaction_add(message, emoji)
        return
    
    matched = _KOISHI_OWO_RP.fullmatch(content,)
    if (matched is not None):
        text = f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
    
    elif (_KOISHI_OMAE_RP.match(content) is not None):
        text = 'NANI?'
    
    else:
        return
    
    await client.message_create(message.channel, text)

Koishi.commands(command_error, checks=[checks.is_guild(DUNGEON)])

@Koishi.commands
async def invalid_command(client, message, command, content):
    prefix = client.command_processer.get_prefix_for(message)
    embed = Embed(
        f'Invalid command `{command}`',
        f'try using: `{prefix}help`',
        color=KOISHI_HELP_COLOR,
            )
    
    message = await client.message_create(message.channel,embed=embed)
    await sleep(30., KOKORO)
    await client.message_delete(message)


@Koishi.commands.from_class
class shutdown:
    async def command(client, message):
        
        for client_ in CLIENTS:
            await client_.disconnect()
        
        await client.message_create(message.channel, 'Clients stopped, stopping process.')
        KOKORO.stop()
        thread_id = main_thread().ident
        signal.pthread_kill(thread_id, signal.SIGKILL)
    
    category = 'UTILITY'
    checks = [checks.owner_only()]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('shutdown', (
            'Shuts the clients down, then stops the process.'
            f'Usage  `{prefix}shutdown`'
            ), color=KOISHI_HELP_COLOR).add_footer(
                'Owner only!')

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
            ), color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')

Koishi.commands(Interpreter(locals().copy()), name='execute', description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])


PATTERN_ROLE_RELATION = [
    (re.compile('nya+', re.I), EVERYNYAN_ROLE, timedelta(minutes=10), True),
    (re.compile('[il] *meow+', re.I), ANNOUNCEMNETS_ROLE, timedelta(), True),
    (re.compile('[il] *not? *meow+', re.I), ANNOUNCEMNETS_ROLE, timedelta(), False),
    (re.compile('nekogirl', re.I), WORSHIPPER_ROLE, timedelta(days=183), True),
        ]

async def role_giver(client, message):
    for pattern, role, delta, add in PATTERN_ROLE_RELATION:
        
        if (pattern.fullmatch(message.content) is None):
            continue
        
        user = message.author
        if add == user.has_role(role):
            break
        
        guild_profile = user.guild_profiles.get(DUNGEON)
        if guild_profile is None:
            break
        
        joined_at = guild_profile.joined_at
        if joined_at is None:
            break
        
        if datetime.utcnow() - joined_at < delta:
            break
        
        permissions = message.channel.cached_permissions_for(client)
        if (not permissions.can_manage_roles) or (not client.has_higher_role_than(role)):
            if permissions.can_send_messages:
                content = 'My permissions are broken, cannot provide the specified role.'
            else:
                break
        else:
            await (Client.user_role_add if add else Client.user_role_delete)(client, user, role)
            
            if permissions.can_send_messages:
                if add:
                    content = f'You now have {role.mention} role.'
                else:
                    content = f'You have {role.mention} removed.'
            
            else:
                break
        
        message = await client.message_create(message.channel, content, allowed_mentions=None)
        await sleep(30.0)
        await client.message_delete(message)
        break

Koishi.command_processer.append(WELCOME_CHANNEL, role_giver)
