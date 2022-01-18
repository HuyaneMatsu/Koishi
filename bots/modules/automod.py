import re
from functools import partial as partial_func

from re import escape as re_escape
from hata import Client, ChannelThread, KOKORO, Permission
from scarletio import Task, WaitTillAll, BUILTIN_EMOJIS
from bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__MODERATOR
from hata.discord.utils import sanitise_mention_escaper

Satori : Client
Koishi: Client

_KOISHI_NOU_RP = re.compile(r'n+\s*o+\s*u+', re.I)
_KOISHI_OWO_RP = re.compile('(owo|uwu|0w0)', re.I)
_KOISHI_OMAE_RP = re.compile('omae wa mou', re.I)

PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)


class RegexPart:
    __slots__ = ('part', )
    def __new__(cls, part):
        part = f'(?:{part})'
        self = object.__new__(cls)
        self.part = part
        return self

class MixedPart:
    __slots__ = ('parts', )
    
    def __new__(cls, *parts):
        self = object.__new__(cls)
        self.parts = parts
        return self
    
    def lower(self):
        new = object.__new__(type(self))
        new.parts = tuple(part.lower() if isinstance(part, str) else part for part in self.parts)
        return new
    
    def __iter__(self):
        for part in self.parts:
            if isinstance(part, str):
                for character in part:
                    yield re_escape(character)
            else:
                yield part.part

def iter_escaped(value):
    if isinstance(value, str):
        for character in value:
            yield re_escape(character)
    else:
        yield from value

FILTERS = (
    'dpy',
    MixedPart(RegexPart('^|\s|`'), 'd.py'),
    MixedPart(RegexPart('^|\s|`'), 'd py'),
    'd_py',
    'd!py',
    'discordpy',
    'discord.py',
    'discord py',
    'discord_py',
    'discord!py',
    'discord.ext',
    'discordr.py',
    'discord\'s py',
    'dp.y',
    'py.discord',
    'D¡\$€0rd.p¥',
    'discord-py',
    'd-py',
    'danny',
    'raptz',
    'rapptz',
    'raprz',
    'pycord',
    'py!cord',
    'py cord',
    'nextcord',
    'pycord-development',
    'discord-interactions',
    'pycord development',
    'discord interactions',
    'discord-ext-views',
    'ditto',
    'migrate',
    'migration',
    'discord.py-message-components',
    'disnake',
    'enhanced-discord.py',
    'novus',
    'fusion.py',
    'pincer',
)

def trie_node_sort_key(node):
    character = node.character
    if character is None:
        character = ''
    
    return character

class TrieNode:
    __slots__ = ('nodes', 'character', 'is_final')
    
    def __init__(self, character):
        self.character = character
        self.nodes = None
        self.is_final = False

    def add(self, word):
        node = self
        nodes = node.nodes
        for character in iter_escaped(word.lower()):
            if (nodes is None):
                nodes = {}
                node.nodes = nodes
            else:
                try:
                    node = nodes[character]
                except KeyError:
                    pass
                else:
                    nodes = node.nodes
                    continue
            
            node = TrieNode(character)
            nodes[character] = node
            nodes = node.nodes
            continue
        
        node.is_final = True
    
    
    def build(self):
        build_to = []
        self._build(build_to)
        return ''.join(build_to)
    
    def _build(self, build_to):
        character = self.character
        if (character is not None):
            build_to.append(character)
        
        nodes = self.nodes
        if (nodes is not None):
            nodes = sorted(nodes.values(), key=trie_node_sort_key)
            
            node_count = len(nodes)
            if node_count == 1:
                if self.is_final:
                    build_to.append('(?:')
                
                node = nodes[0]
                node._build(build_to)
                
                if self.is_final:
                    build_to.append(')?')
            
            else:
                build_to.append('(?:')
                
                node_index = 0
                
                while True:
                    node = nodes[node_index]
                    node_index += 1
                    
                    node._build(build_to)
                    
                    if node_index == node_count:
                        break
                    
                    build_to.append('|')
                    continue
                
                build_to.append(')')
                
                if self.is_final:
                    build_to.append('?')


def build_auto_mod():
    node = TrieNode(None)
    for word in FILTERS:
        node.add(word)
    
    regex_pattern = re.compile(node.build(), re.I | re.M | re.S | re.U,)
    
    return regex_pattern

FILTER = build_auto_mod()

class Replacer:
    __slots__ = ('called', )
    
    def __init__(self):
        self.called = False
    
    def __call__(self, regex_match):
        self.called = True
        return 'meow'


@Satori.events
async def message_create(client, message):
    if message.guild_id != GUILD__SUPPORT.id:
        return
    
    if await filter_content(client, message):
        return
    
    await alter_content(client, message)


@Satori.events
async def message_edit(client, message, old_attributes):
    if message.guild_id != GUILD__SUPPORT.id:
        return
    
    await filter_content(client, message)


async def replace_coroutine(client, message, content):
    channel = message.channel
    if isinstance(channel, ChannelThread):
        channel_id = channel.parent_id
        thread = channel
    else:
        channel_id = channel.id
        thread = None
    
    executor_webhook = await client.webhook_get_own_channel(channel_id)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel_id, 'auto_mod')
    
    user = message.author
    
    await client.webhook_message_create(
        executor_webhook,
        content,
        allowed_mentions = None,
        thread = thread,
        name = user.name_at(message.guild),
        avatar_url = user.avatar_url,
    )


async def filter_content(client, message):
    user = message.author
    if user.is_bot or user.has_role(ROLE__SUPPORT__MODERATOR):
        return False
    
    content = message.content
    if (content is None):
        return False
    
    replacer = Replacer()
    content = FILTER.sub(replacer, content)
    
    if not replacer.called:
        return False
    
    delete_task = Task(client.message_delete(message), KOKORO)
    replace_task = Task(replace_coroutine(client, message, content), KOKORO)
    await WaitTillAll([delete_task, replace_task], KOKORO)
    
    try:
        delete_task.result()
    except ConnectionError:
        pass
    
    try:
        replace_task.result()
    except ConnectionError:
        pass
    
    return True



async def alter_content(client, message):
    if (message.referenced_message is not None):
        return False
    
    if not message.channel.cached_permissions_for(Koishi) & PERMISSION_MASK_MESSAGING:
        return False
    
    if message.author.is_bot:
        return False
    
    content = message.content
    if content is None:
        return False
    
    user_mentions = message.user_mentions
    if (user_mentions is not None) and (Koishi in user_mentions):
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
        await Koishi.message_create(message.channel, result, allowed_mentions=[author])
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
