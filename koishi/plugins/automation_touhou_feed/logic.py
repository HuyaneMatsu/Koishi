__all__ = ('try_remove_guild', 'try_update_guild')

from itertools import chain
from random import choice, random

from hata import Client, DiscordException, ERROR_CODES, Embed, KOKORO, now_as_id
from scarletio import CancelledError, LOOP_TIME, Task

from ...bots import SLASH_CLIENT

from ..automation_core import get_touhou_feed_enabled
from ..touhou_core import TouhouHandlerKey, get_touhou_character_like, parse_touhou_characters_from_tags

from .constants import (
    DEFAULT_INTERVAL, FEEDERS, INTERVAL_RP, INTERVAL_UNIT_RP, MAX_INTERVAL, MIN_INTERVAL, TAG_NAME_REQUIRED,
    TAG_NAME_SOLO, TAG_REQUIRED_RP, TAG_ITER_RP
)



def iter_tag_names_of(channel):
    """
    Iterates over the tags' names of the given channel.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to iterate it's tags over.
    """
    yield channel.name
    
    if channel.is_guild_text():
        topic = channel.topic
        if (topic is not None):
            yield from TAG_ITER_RP.findall(topic)
    
    elif channel.is_guild_thread_public():
        for tag in channel.iter_applied_tags():
            yield tag.name


def try_parse_handler_key(tag_name):
    """
    Parses the given tag name and returns a created handler key from it if applicable.
    
    Parameters
    ----------
    tag_name : `str`
        The tag's name.
    
    Returns
    -------
    handler_key : `None`, ``TouhouHandlerKey``
    """
    solo = False
    characters = None
    
    for split in tag_name.split('+'):
        split = split.strip()
        if split == TAG_NAME_SOLO:
            solo = True
            continue
        
        character = get_touhou_character_like(split)
        if (character is not None):
            if characters is None:
                characters = []
            
            characters.append(character)
    
    if characters is not None:
        return TouhouHandlerKey(*characters, solo = solo)


def try_parse_interval(tag_name):
    """
    Tries to parse interval out from the given tag name.
    
    Parameters
    ----------
    tag_name : `str`
        The tag's name.
    
    Returns
    -------
    interval : `int`
    """
    match = INTERVAL_RP.fullmatch(tag_name)
    if match is None:
        return 0
    
    interval = match.group(1)
    
    hours = 0
    minutes = 0
    seconds = 0
    
    for math in INTERVAL_UNIT_RP.finditer(interval):
        duration, unit = math.groups()
        if len(duration) > 2:
            duration = 99
        else:
            duration = int(duration)
        
        if unit == 'h':
            if duration > 24:
                hours = 24
            else:
                hours = duration
        
        elif unit == 'm':
            if duration > 59:
                minutes = 0
            else:
                minutes = duration
        
        elif unit == 's':
            if duration > 59:
                seconds = 0
            else:
                seconds = duration
    
    return hours * 3600 + minutes * 60 + seconds


def parse_channel_tags(channel):
    """
    Gets the handler key for the given channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to get it's key of.
    
    Returns
    -------
    handler_keys_and_interval : `None`, `tuple` ((`tuple` of ``TouhouHandlerKey``), `int`)
    """
    handler_keys = None
    final_interval = 0
    solo_only = False
    required_tag_found = False
    
    for tag_name in iter_tag_names_of(channel):
        if tag_name == TAG_NAME_REQUIRED:
            required_tag_found = True
            continue
        
        if tag_name == TAG_NAME_SOLO:
            solo_only = True
            continue
        
        interval = try_parse_interval(tag_name)
        if interval:
            final_interval = interval
            continue
        
        handler_key = try_parse_handler_key(tag_name)
        if (handler_key is not None):
            if (handler_keys is None):
                handler_keys = []
            
            handler_keys.append(handler_key)
            continue
    
    
    if (handler_keys is not None):
        if solo_only:
            for handler_key in handler_keys:
                handler_key.apply_solo_preference()
        
        return tuple(handler_keys), normalise_interval(final_interval)
    
    if required_tag_found:
        return (TouhouHandlerKey(solo = solo_only),), normalise_interval(final_interval)


def normalise_interval(interval):
    """
    Normalises the given interval.
    
    Parameters
    ----------
    interval : `int`
        The defined interval.
    
    Returns
    -------
    interval : `int`
    """
    if interval == 0:
        interval = DEFAULT_INTERVAL
    
    elif interval < MIN_INTERVAL:
        interval = MIN_INTERVAL
    
    elif interval > MAX_INTERVAL:
        interval = MAX_INTERVAL
    
    return interval


def join_names_of_touhou_characters(characters, join_with):
    """
    Joins the given character's names.
    
    Parameters
    ----------
    characters : `set<TouhouCharacter>`
        The touhou character names to join.
    join_with : `str`
        The string to join the names with.
    
    Returns
    -------
    joined_names : `None`, `str`
    """
    if characters is None:
        character_count = 0
    else:
        character_count = len(characters)
    
    if character_count == 0:
        return '*none*'
    
    characters = sorted(characters)
    
    if character_count > 10:
        dropped = character_count - 10
        character_count = 10
        del characters[10:]
    
    else:
        dropped = None
    
    built = []
    
    index = 0
    while True:
        character = characters[index]
        index += 1
        
        built.append(character.name)
        
        if index == character_count:
            break
        
        built.append(join_with)
        continue
    
    if dropped:
        built.append(join_with)
        built.append('... +')
        built.append(str(dropped))
    
    return ''.join(built)


def should_touhou_feed_in_channel(client, channel):
    """
    Returns whether the client should try to auto post in the given channel.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post in the channel.
    channel : ``Channel``
        The channel to check.
    
    Returns
    -------
    should : `bool`
    """
    if channel.is_guild_text():
        topic = channel.topic
        if topic is None:
            return False
        
        if not channel.cached_permissions_for(client).can_send_messages:
            return False
        
        if TAG_REQUIRED_RP.search(topic) is not None:
            return True
        
        return False
    
    if channel.is_guild_thread_public():
        parent = channel.parent
        if (parent is None):
            return False
        
        if not parent.is_in_group_forum():
            return False
        
        if not parent.cached_permissions_for(client).can_send_messages_in_threads:
            return False
        
        for tag in channel.iter_applied_tags():
            if tag.name == TAG_NAME_REQUIRED:
                return True
        
        return False
    
    return False


def get_interval_only(channel):
    """
    Gets the channel's interval only.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to gets its interval of.
    
    Returns
    -------
    interval : `int`
    """
    final_interval = 0
    
    for tag_name in iter_tag_names_of(channel):
        if tag_name == TAG_NAME_REQUIRED:
            continue
        
        interval = try_parse_interval(tag_name)
        if interval:
            final_interval = interval
    
    return normalise_interval(final_interval)


class Feeder:
    """
    Auto channel feeder.
    
    Attributes
    ----------
    channel : ``Channel``
        The channel to auto post at.
    handle : `None`, ``TimerHandle``
        The current handle of the auto poster.
    handler_keys : `tuple` of ``TouhouHandlerKey``
        Handler keys which handle which characters should be posted.
    interval : `int`
        The interval between posting in seconds.
    """
    __slots__ = ('channel', 'handle', 'handler_keys', 'interval')
    
    def __new__(cls, channel):
        """
        Creates a new feeder instance.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel to auto post at.
        """
        handler_keys_and_interval = parse_channel_tags(channel)
        if handler_keys_and_interval is None:
            return
        
        self = object.__new__(cls)
        self.channel = channel
        self.handle = None
        self.handler_keys, self.interval = handler_keys_and_interval
        
        self.schedule()
        FEEDERS[channel.id] = self
        
        return self
    
    
    def __repr__(self):
        """Returns the feeder's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channel = ')
        repr_parts.append(repr(self.channel))
        
        repr_parts.append(', handler_keys = ')
        repr_parts.append(repr(self.handler_keys))
        
        repr_parts.append(', interval = ')
        repr_parts.append(repr(self.interval))
        
        handle = self.handle
        if (handle is not None) and (not handle.cancelled):
            repr_parts.append(', till next call: ')
            repr_parts.append(format(handle.when - LOOP_TIME(), '.0f'))
            repr_parts.append(' seconds')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def update(self):
        """
        Updates the feeder.
        """
        handler_keys_and_interval = parse_channel_tags(self.channel)
        if handler_keys_and_interval is None:
            self.cancel()
        
        else:
            self.handler_keys, self.interval = handler_keys_and_interval
            self.re_schedule()
    
    
    def schedule(self):
        """
        Schedules the feeder.
        
        If called while scheduled, it will break the scheduled.
        """
        self.handle = KOKORO.call_after(self.interval, self.invoke)
    
    
    def re_schedule(self):
        """
        Schedules the feeder.
        
        If the feeder is already scheduled, it might cancel the old scheduling.
        """
        call_at = LOOP_TIME() + self.interval
        
        current_handle = self.handle
        if (current_handle is not None) and (not current_handle.cancelled):
            if current_handle.when <= call_at:
                return
            
            current_handle.cancel()
        
        self.handle = KOKORO.call_at(call_at, self.invoke)
    
    
    def cancel(self):
        """
        Cancels the schedule.
        """
        handle = self.handle
        if (handle is not None):
            handle.cancel()
            self.handle = None
        
        channel_id = self.channel.id
        if FEEDERS.get(channel_id, None) is self:
            del FEEDERS[channel_id]
    
    
    def invoke(self):
        """
        Triggers a feed.
        """
        self.schedule()
        Task(KOKORO, self.execute())
    
    
    async def execute(self):
        """
        Executes a feed.
        
        This method is a coroutine.
        """
        try:
            # SKip images if there are too many characters on it. Do 5 retries.
            retries = 5
            while True:
                image_detail = await choice(self.handler_keys).get_handler().get_image(SLASH_CLIENT, None)
                if (image_detail is None):
                    return
                
                touhou_characters = parse_touhou_characters_from_tags(image_detail)
                
                retries -= 1
                if retries <= 0:
                    break
                
                if len(touhou_characters) > 12 and random() > 0.2:
                    continue
                
                break
            
            title = join_names_of_touhou_characters(touhou_characters, ', ')
            
            embed = Embed(
                title,
                url = image_detail.url,
                color = (now_as_id() >> 22) & 0xffffff,
            ).add_image(
                image_detail.url,
            )
            
            try:
                await SLASH_CLIENT.message_create(self.channel, embed = embed)
            except ConnectionError:
                pass
            
            except DiscordException as err:
                if err.status >= 500:
                    return
                
                if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.rate_limit_slowmode, # slowmode
                ):
                    self.cancel()
                
                raise
        
        except (GeneratorExit, CancelledError):
            raise
        
        except BaseException as err:
            await SLASH_CLIENT.events.error(SLASH_CLIENT, repr(self), err)


def try_update_channel(channel):
    """
    Updates the channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The respective channel instance.
    """
    try:
        feeder = FEEDERS[channel.id]
    except KeyError:
        Feeder(channel)
    else:
        feeder.update()


def try_remove_channel(channel):
    """
    Tries to remove only the channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The respective channel instance.
    """
    try:
        feeder = FEEDERS[channel.id]
    except KeyError:
        pass
    else:
        feeder.cancel()


def try_update_guild(client, guild):
    """
    Scans the guild for touhou-feed channels to update them.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    guild : ``Guild``
        The guild to scan.
    """
    for channel in chain(guild.channels.values(), guild.threads.values()):
        if should_touhou_feed_in_channel(client, channel):
            try_update_channel(channel)


def try_remove_guild(guild):
    """
    Scans the guild for touhou-feed channels to remove them.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    guild : ``Guild``
        The guild to scan.
    """
    for channel in chain(guild.channels.values(), guild.threads.values()):
         try_remove_channel(channel)


def reset_touhou_feeders(client):
    """
    Resets all auto posters. Removing the old ones and adding the new ones.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    """
    for guild in SLASH_CLIENT.guilds:
        if get_touhou_feed_enabled(guild.id):
            for channel in chain(guild.channels.values(), guild.threads.values()):
                reset_channel_single(client, channel)


def reset_channel(client, channel):
    """
    Resets the given channel of auto posting. If the channel is a guild forum, it goes through all of its threads.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    channel : ``Channel``
        The channel to reset.
    """
    if channel.is_in_group_forum():
        for thread in channel.iter_threads():
            reset_channel_single(client, thread)
    
    else:
        reset_channel_single(client, channel)


def reset_channel_single(client, channel):
    """
    Resets the given channel of auto posting. Not like ``reset_channel`` this does check only the channel.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    channel : ``Channel``
        The channel to reset.
    """
    if should_touhou_feed_in_channel(client, channel):
        try_update_channel(channel)
    else:
        try_remove_channel(channel)


def setup(lib):
    """
    Called after the plugin is loaded.
    
    Parameters
    ----------
    lib : `ModuleType`
        This module.
    """
    reset_touhou_feeders(SLASH_CLIENT)


def teardown(lib):
    """
    Called before the plugin is destroyed.
    
    Parameters
    ----------
    lib : `ModuleType`
        This module.
    """
    for feeder in [*FEEDERS.values()]:
        feeder.cancel()
