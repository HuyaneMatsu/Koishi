import re
from re import escape as re_escape

from hata import Client, BUILTIN_EMOJIS, ChannelThread, Task, KOKORO, WaitTillAll

from bot_utils.constants import GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__MODERATOR

Satori : Client

FILTERS = (
    'dpy',
    'd.py',
    'd py',
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
        for character in word.lower():
            character = re_escape(character)
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
    
    regex_pattern = re.compile(node.build(), re.I|re.M|re.S|re.U,)
    
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
    await filter(client, message)

@Satori.events
async def message_edit(client, message, old_attributes):
    await filter(client, message)


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


async def filter(client, message):
    if message.guild_id != GUILD__NEKO_DUNGEON.id:
        return
    
    user = message.author
    if user.is_bot or user.has_role(ROLE__NEKO_DUNGEON__MODERATOR):
        return
    
    content = message.content
    if (content is None):
        return
    
    replacer = Replacer()
    content = FILTER.sub(replacer, content)
    
    if not replacer.called:
        return
    
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
