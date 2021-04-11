# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

from hata import BUILTIN_EMOJIS, sleep,  Client, KOKORO, cchunkify, alchemy_incendiary
from hata.ext.command_utils import setup_ext_command_utils
from hata.ext.slash import setup_ext_slash
from hata.backend.futures import render_exc_to_list

from bot_utils.tools import MessageDeleteWaitfor, GuildDeleteWaitfor, RoleDeleteWaitfor, ChannelDeleteWaitfor, \
    EmojiDeleteWaitfor, RoleEditWaitfor, ChannelCreateWaitfor, ChannelEditWaitfor
from bot_utils.shared import CHANNEL__NEKO_DUNGEON__SYSTEM, GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, \
    ROLE__NEKO_DUNGEON__ELEVATED, CHANNEL__SYSTEM__SYNC, ROLE__NEKO_DUNGEON__VERIFIED, \
    CHANNEL__NEKO_DUNGEON__DEFAULT_TEST, ROLE__NEKO_DUNGEON__NSFW_ACCESS


from bot_utils.syncer import sync_request_waiter

_KOISHI_NOU_RP = re.compile(r'n+\s*o+\s*u+', re.I)
_KOISHI_OWO_RP = re.compile('(owo|uwu|0w0)', re.I)
_KOISHI_OMAE_RP = re.compile('omae wa mou', re.I)

Koishi: Client

setup_ext_command_utils(Koishi)
setup_ext_slash(Koishi)

Koishi.events.message_create.append(CHANNEL__SYSTEM__SYNC, sync_request_waiter)

Koishi.events(MessageDeleteWaitfor)
Koishi.events(GuildDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(ChannelDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleEditWaitfor)
Koishi.events(ChannelCreateWaitfor)
Koishi.events(ChannelEditWaitfor)


@Koishi.events
async def message_create(client, message):
    if (message.referenced_message is not None):
        return
    
    if not message.channel.cached_permissions_for(client).can_send_messages:
        return
    
    if message.author.is_bot:
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


PATTERN_ROLE_RELATION = [
    (re.compile('nya+', re.I), ROLE__NEKO_DUNGEON__VERIFIED, timedelta(minutes=10), True, False),
    (re.compile('[il] *meow+', re.I), ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, None, True, False),
    (re.compile('[il] *not? *meow+', re.I), ROLE__NEKO_DUNGEON__ANNOUNCEMENTS, None, False, False),
    (re.compile('nekogirl', re.I), ROLE__NEKO_DUNGEON__ELEVATED, timedelta(days=183), True, True),
    (re.compile('(?:i(?: *\'? *am|mma)?|me)? *horny *(?:desu)?', re.I), ROLE__NEKO_DUNGEON__NSFW_ACCESS, None, True, True),
    (re.compile('no *sex', re.I), ROLE__NEKO_DUNGEON__NSFW_ACCESS, None, False, True),
        ]

async def role_giver(client, message):
    for pattern, role, delta, add, requires_verify in PATTERN_ROLE_RELATION:
        
        if (pattern.fullmatch(message.content) is None):
            continue
        
        user = message.author
        if requires_verify and (not user.has_role(ROLE__NEKO_DUNGEON__VERIFIED)):
            break
        
        if add == user.has_role(role):
            break
        
        guild_profile = user.guild_profiles.get(GUILD__NEKO_DUNGEON, None)
        if guild_profile is None:
            break
        
        joined_at = guild_profile.joined_at
        if joined_at is None:
            break
        
        if (delta is not None) and (datetime.utcnow() - joined_at < delta):
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
        await sleep(30.0, KOKORO)
        await client.message_delete(message)
        break

Koishi.events.message_create.append(CHANNEL__NEKO_DUNGEON__SYSTEM, role_giver)

@Koishi.events(overwrite=True)
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

