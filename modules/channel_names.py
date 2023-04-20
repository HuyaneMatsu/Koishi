__all__ = ()

import os
from csv import reader as CSVReader, writer as CSVWriter
from time import time as time_now
from random import random
from datetime import datetime
from difflib import get_close_matches

from bot_utils.constants import CATEGORY__SUPPORT__BOTS, PATH__KOISHI, ROLE__SUPPORT__MODERATOR
from bot_utils.tools import Cell

from hata import KOKORO, Embed, Client, BUILTIN_EMOJIS
from scarletio import Lock, alchemy_incendiary, Task
from hata.ext.slash import Button, Row, wait_for_component_interaction
from hata.ext.slash.menus import Pagination, Closer
from hata.ext.commands_v2 import checks

FILE_NAME = 'channel_names.csv'

FILE_PATH = os.path.join(PATH__KOISHI, 'bots', 'modules', FILE_NAME)
FILE_LOCK = Lock(KOKORO)
EDIT_LOCK = Lock(KOKORO)

DEFAULT_NAME = 'go-go-maniac'

DAY = 24.0 * 60.0 * 60.0
DAY_CHANCE_MULTIPLIER = 0.01 / DAY

SPACE_CHAR = '-'

CHANNEL_CHAR_TABLE = {}
for source, target in (
    ('!', 'ǃ'),
    ('?', '？'),
):
    CHANNEL_CHAR_TABLE[source] = target
    CHANNEL_CHAR_TABLE[target] = target

# Add quote chars
for char in ('\'', '`', '"'):
    CHANNEL_CHAR_TABLE[char] = '’'

# Add space chars
for char in (' ', '-', '\t', '\n', '~'):
    CHANNEL_CHAR_TABLE[char] = SPACE_CHAR

# Add lowercase letters
for char in range(b'a'[0], b'z'[0] + 1):
    char = chr(char)
    CHANNEL_CHAR_TABLE[char] = char

# Add uppercase letters
for shift in range(0, b'Z'[0] - b'A'[0] + 1):
    source = chr(b'A'[0] + shift)
    target = chr(ord('𝖠') + shift)
    CHANNEL_CHAR_TABLE[source] = target
    CHANNEL_CHAR_TABLE[target] = target

# Add numbers
for char in range(b'0'[0], b'9'[0] + 1):
    char = chr(char)
    CHANNEL_CHAR_TABLE[char] = char

# Cleanup
del shift, target, source, char


def escape_name(name):
    created = []
    last = SPACE_CHAR
    for char in name:
        char = CHANNEL_CHAR_TABLE.get(char, None)
        if char is None:
            continue
        
        if char == SPACE_CHAR and last == SPACE_CHAR:
            continue
        
        created.append(char)
        last = char
    
    if created and created[-1] == SPACE_CHAR:
        del created[-1]
    
    return ''.join(created)


class ChannelNameDescriber:
    __slots__ = ('_chance', 'last_present', 'name', 'weight')
    
    @classmethod
    def from_csv_line(cls, line):
        name, last_present, weight = line
        
        last_present = int(last_present, base=16)
        weight = int(weight, base=16)
        
        self = object.__new__(cls)
        
        self.name = name
        self.last_present = last_present
        self.weight = weight
        self._chance = None
        
        return self
    
    @classmethod
    def from_name_and_weight(cls, name, weight):
        self = object.__new__(cls)
        
        self.name = name
        self.last_present = int(time_now())
        self.weight = weight
        self._chance = None
        
        return self
    
    @property
    def chance(self):
        chance = self._chance
        if chance is None:
            self._chance = chance = (1.0 + (time_now() - self.last_present) * DAY_CHANCE_MULTIPLIER) * self.weight
        
        return chance
    
    def __len__(self):
        return 3
    
    def __iter__(self):
        yield self.name
        yield self.last_present.__format__('X')
        yield self.weight.__format__('X')
    
    def present(self):
        self.last_present = int(time_now())
        self._chance = 0.0


async def get_random_names(count):
    names = await read_channels()
    chosen = []
    if len(names) <= count:
        for describer in names:
            chosen.append(describer.name)
            describer.present()
        
        for _ in range(len(names), count):
            chosen.append(DEFAULT_NAME)
    
    else:
        total_chance = 0.0
        for describer in names:
            total_chance += describer.chance
        
        for _ in range(count):
            position = total_chance * random()
            
            # Add some extra for security issues. If the first name was selected and `random()` returns `0.0`, then
            # the same name could be selected twice.
            if position == 0.0:
                position = 0.01
            
            for describer in names:
                chance = describer.chance
                position -= chance
                if position > 0.0:
                    continue
                
                total_chance -= chance
                describer.present()
                chosen.append(describer.name)
                break
    
    await write_channels(names)
    return chosen


def read_channels_task():
    names = []
    if not os.path.exists(FILE_PATH):
        return names
    
    with open(FILE_PATH, 'r') as file:
        reader = CSVReader(file)
        for line in reader:
            describer = ChannelNameDescriber.from_csv_line(line)
            names.append(describer)
    
    return names


def write_channels_task(names):
    with open(FILE_PATH, 'w') as file:
        writer = CSVWriter(file)
        writer.writerows(names)


async def read_channels():
    async with FILE_LOCK:
        return await KOKORO.run_in_executor(read_channels_task)


async def write_channels(names):
    async with FILE_LOCK:
        await KOKORO.run_in_executor(alchemy_incendiary(write_channels_task, (names,)))


async def do_rename():
    async with EDIT_LOCK:
        if not CATEGORY__SUPPORT__BOTS.guild.permissions_for(COMMAND_CLIENT).can_manage_channels:
            return
        
        channels = CATEGORY__SUPPORT__BOTS.channels
        count = len(channels)
        if not count:
            return
        
        names = await get_random_names(count)
        
        for channel, name in zip(channels, names):
            await COMMAND_CLIENT.channel_edit(channel, name = name)


def cycle_rename():
    NAME_CYCLER_HANDLER.value = KOKORO.call_later(DAY, cycle_rename)
    Task(do_rename(), KOKORO)

NAME_CYCLER_HANDLER = Cell()

COMMAND_CLIENT: Client
COMMAND_CLIENT.command_processor.create_category('CHANNEL NAMES', checks = [checks.has_role(ROLE__SUPPORT__MODERATOR)])

def setup(lib):
    NAME_CYCLER_HANDLER.value = KOKORO.call_later(
        datetime.utcnow().replace(microsecond=0, second=0, minute=0, hour=0).timestamp() - time_now() + DAY,
        cycle_rename,
    )

def teardown(lib):
    value = NAME_CYCLER_HANDLER.value
    if (value is not None):
        NAME_CYCLER_HANDLER.value = None
        value.cancel()


@COMMAND_CLIENT.commands(category='CHANNEL NAMES')
async def list_bot_channel_names(client, message):
    """
    Lists the already added bot channel names.
    """
    names = await read_channels()
    
    descriptions = []
    if names:
        lines = []
        page_size = 0
        for index, describer in enumerate(names, 1):
            if page_size == 16:
                description = '\n'.join(lines)
                descriptions.append(description)
                lines.clear()
                page_size = 0
            else:
                page_size += 1
                line = f'{index}. [{describer.weight}] {describer.name}'
                lines.append(line)
        
        if page_size:
            description = '\n'.join(lines)
            descriptions.append(description)
            lines.clear()
    else:
        descriptions.append('*none*')
    
    pages = [Embed('Bot channel names', description) for description in descriptions]
    await Pagination(client, message.channel, pages)


def check_staff_role(event):
    return event.user.has_role(ROLE__SUPPORT__MODERATOR)

ADD_EMOJI_OK = BUILTIN_EMOJIS['ok_hand']
ADD_EMOJI_CANCEL = BUILTIN_EMOJIS['x']

ADD_BUTTON_OK = Button(emoji = ADD_EMOJI_OK)
ADD_BUTTON_CANCEL = Button(emoji = ADD_EMOJI_CANCEL)

ADD_COMPONENTS = Row(ADD_BUTTON_OK, ADD_BUTTON_CANCEL)

@COMMAND_CLIENT.commands(category='CHANNEL NAMES', separator='|')
async def add_bot_channel_name(client, message, weight:int, name):
    """
    Adds the given channel name to the bot channel names.
    
    When adding a command please also define weight and not only name as: `weight | name`
    """
    if EDIT_LOCK.is_locked():
        await Closer(client, message.channel, Embed('Ohoho', 'A bot channel editing is already taking place.'))
        return
    
    async with EDIT_LOCK:
        name = escape_name(name)
        if not 2 <= len(name) <= 100:
            await Closer(client, message.channell, Embed(f'Too long or short name', name))
            return
        
        names = await read_channels()
        close_matches = get_close_matches(name, [describer.name for describer in names], n=1, cutoff=0.8)
        if not close_matches:
            overwrite = False
            embed = Embed(
                'Add bot channel name',
                f'Would you like to add a channel name:\n{name}\nWith weight of {weight}.',
            )
        elif close_matches[0] == name:
            overwrite = True
            embed = Embed(
                'Add bot channel name',
                (
                    f'Would you like to overwrite the following bot channel name:\n'
                    f'{name}\n'
                    f'To weight of {weight}.'
                ),
            )
        else:
            overwrite = False
            embed = Embed(
                'Add bot channel name',
                (
                    f'There is a familiar channel name already added: {close_matches[0]}\n'
                    f'Would you like to overwrite the following bot channel name:\n'
                    f'{name}\n'
                    f'To weight of {weight}.'
                ),
            )
        
        message = await client.message_create(message.channel, embed = embed, components = ADD_COMPONENTS)
        
        try:
            event = await wait_for_component_interaction(message, timeout = 300., check = check_staff_role)
        except TimeoutError:
            event = None
            cancelled = False
        else:
            cancelled = (event.interaction == ADD_BUTTON_CANCEL)
        
        if cancelled:
            footer = 'Name adding cancelled.'
        else:
            if overwrite:
                for describer in names:
                    if describer.name == describer:
                        describer.weight = weight
                
                footer = 'Name overwritten successfully.'
            else:
                describer = ChannelNameDescriber.from_name_and_weight(name, weight)
                names.append(describer)
                footer = 'Name added successfully.'
            await write_channels(names)
        
        embed.add_footer(footer)
        
        if event is None:
            await client.message_edit(message, embed = embed, components = None)
        else:
            await client.interaction_component_message_edit(event, embed = embed, components = None)


@COMMAND_CLIENT.commands(category='CHANNEL NAMES')
async def do_bot_channel_rename(client, message):
    """
    Adds the given channel name to the bot channel names.
    
    When adding a command please also define weight and not only name as: `weight | name`
    """
    await do_rename()
    await Closer(client, message.channel, Embed(description = 'Rename done'))
