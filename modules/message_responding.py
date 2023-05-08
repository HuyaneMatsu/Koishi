__all__ = ()

import re
from functools import partial as partial_func
from re import escape as re_escape

from hata import BUILTIN_EMOJIS, Permission
from hata.discord.utils import sanitise_mention_escaper

from bot_utils.constants import GUILD__SUPPORT
from bots import Koishi, Satori


_KOISHI_NOU_RP = re.compile('n+\s*o+\s*u+', re.I)
_KOISHI_OWO_RP = re.compile('(owo|uwu|0w0)', re.I)
_KOISHI_OMAE_RP = re.compile('omae wa mou', re.I)


PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)


@Satori.events
async def message_create(client, message):
    if message.guild_id != GUILD__SUPPORT.id:
        return
    
    await alter_content(client, message)


async def alter_content(client, message):
    if (message.referenced_message is not None):
        return False
    
    if not message.channel.cached_permissions_for(Koishi) & PERMISSION_MASK_MESSAGING:
        return False
    
    if message.author.bot:
        return False
    
    content = message.content
    if content is None:
        return False
    
    mentioned_users = message.mentioned_users
    if (mentioned_users is not None) and (Koishi in mentioned_users):
        author = message.author
        m1 = author.mention
        m2 = Koishi.mention
        m3 = author.mention_nick
        m4 = Koishi.mention_nick
        replace = {
            '@everyone'   : '@\u200beveryone',
            '@here'       : '@\u200bhere',
            re_escape(m1) : m2,
            re_escape(m2) : m1,
            re_escape(m3) : m4,
            re_escape(m4) : m3,
        }
        pattern = re.compile('|'.join(replace.keys()))
        result = pattern.sub(partial_func(sanitise_mention_escaper, replace), content)
        await Koishi.message_create(message.channel, result, allowed_mentions = [author])
        return True
        
    if message.channel.cached_permissions_for(Koishi).can_add_reactions and (_KOISHI_NOU_RP.match(content) is not None):
        for value in 'nou':
            emoji = BUILTIN_EMOJIS[f'regional_indicator_{value}']
            await Koishi.reaction_add(message, emoji)
        
        return True
    
    matched = _KOISHI_OWO_RP.fullmatch(content,)
    if (matched is not None):
        text = f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
    
    elif (_KOISHI_OMAE_RP.match(content) is not None):
        text = 'NANI?'
    
    else:
        return False
    
    await Koishi.message_create(message.channel, text)
    return True
