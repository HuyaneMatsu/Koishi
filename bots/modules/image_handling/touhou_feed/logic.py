__all__ = ()

from itertools import chain

from hata import Client, DiscordException, ERROR_CODES, Embed, KOKORO, now_as_id
from scarletio import CancelledError, LOOP_TIME, Task

from ..touhou import TouhouHandlerKey, get_touhou_character_like, parse_touhou_characters_from_tags

from .constants import (
    DEFAULT_INTERVAL, FEEDERS, INTERVAL_MULTIPLIER, MAX_INTERVAL, MIN_INTERVAL, TAG_NAME_REQUIRED, TAG_NAME_SOLO,
    TAG_REQUIRED_RP, TAG_RP
)


SLASH_CLIENT: Client


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
            yield from TAG_RP.findall(topic)
    
    elif channel.is_guild_thread_public():
        for tag in channel.iter_applied_tags():
            yield tag.name



def get_channel_handler_key(channel):
    """
    Gets the handler key for the given channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to get it's key of.
    
    Returns
    -------
    handler_key : `None`, ``TouhouHandlerKey``
    """
    solo = False
    characters = []
    
    for tag_name in iter_tag_names_of(channel):
        touhou_character = get_touhou_character_like(tag_name)
        if tag_name == TAG_NAME_SOLO:
            solo = True
            continue
        
        if tag_name == TAG_NAME_REQUIRED:
            continue
        
        if (touhou_character is not None):
            characters.append(touhou_character)
    
    if characters:
        return TouhouHandlerKey(*characters, solo = solo)


def get_feed_interval(channel):
    """
    Gets the post interval of a channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The respective channel.
    
    Returns
    -------
    interval : `int`
    """
    return slowmode_to_interval(channel.slowmode)


def slowmode_to_interval(slowmode):
    """
    Converts the given slowmode to interval.
    
    Parameters
    ----------
    slowmode : `int`
        A channel's slowmode.
    
    Returns
    -------
    interval : `int`
    """
    if not slowmode:
        interval = DEFAULT_INTERVAL
    
    else:
        interval = slowmode * INTERVAL_MULTIPLIER
        
        if interval < MIN_INTERVAL:
            interval = MIN_INTERVAL
        
        elif interval > MAX_INTERVAL:
            interval = MAX_INTERVAL
    
    return interval


def join_names_of_touhou_characters(characters, join_with):
    """
    Joins the given character's names.
    
    Parameters
    ----------
    characters : `set` of ``TouhouCharacter``
        The touhou character names to join.
    join_with : `str`
        The string to join the names with.
    
    Returns
    -------
    joined_names : `None`, `str`
    """
    character_count = len(characters)
    if character_count == 0:
        return None
    
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


def should_auto_post_in_channel(client, channel):
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
        
        if not parent.is_guild_forum():
            return False
        
        if not parent.cached_permissions_for(client).can_send_messages_in_threads:
            return False
        
        for tag in channel.iter_applied_tags():
            if tag.name == TAG_NAME_REQUIRED:
                return True
        
        return False
    
    return False


class Feeder:
    """
    Auto channel feeder.
    
    Attributes
    ----------
    channel : ``Channel``
        The channel to auto post at.
    handle : `None`, ``TimerHandle``
        The current handle of the auto poster.
    handler_key : ``TouhouHandlerKey``
        Handler key which handles which characters should be posted.
    """
    __slots__ = ('channel', 'handle', 'handler_key',)
    
    def __new__(cls, channel):
        """
        Creates a new feeder instance.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel to auto post at.
        """
        handler_key = get_channel_handler_key(channel)
        if handler_key is None:
            return
        
        self = object.__new__(cls)
        self.channel = channel
        self.handle = None
        self.handler_key = handler_key
        
        self.schedule()
        FEEDERS[channel.id] = self
        
        return self
    
    
    def __repr__(self):
        """Returns the feeder's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channel = ')
        repr_parts.append(repr(self.channel))
        
        repr_parts.append(', handler_key = ')
        repr_parts.append(repr(self.handler_key))
        
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
        handler_key = get_channel_handler_key(self.channel)
        if handler_key is None:
            self.cancel()
        
        else:
            self.handler_key = handler_key
            self.re_schedule()
    
    
    def schedule(self):
        """
        Schedules the feeder.
        
        If called while scheduled, it will break the scheduled.
        """
        self.handle = KOKORO.call_later(get_feed_interval(self.channel), self.invoke)
    
    
    def re_schedule(self):
        """
        Schedules the feeder.
        
        If the feeder is already scheduled, it might cancel the old scheduling.
        """
        call_at = LOOP_TIME() + get_feed_interval(self.channel)
        
        current_handle = self.handle
        if (current_handle is not None) and (not current_handle.cancelled):
            if current_handle.when < call_at:
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
        Task(self.execute(), KOKORO)
    
    
    async def execute(self):
        """
        Executes a feed.
        
        This method is a coroutine.
        """
        try:
            image_detail = await self.handler_key.get_handler().get_image(SLASH_CLIENT, None)
            if (image_detail is None):
                return
            
            title = join_names_of_touhou_characters(parse_touhou_characters_from_tags(image_detail), ', ')
            
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
                if err.code not in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.rate_limit_slowmode, # slowmode
                ):
                    raise
                
                self.cancel()
        
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


def reset_auto_posters(client):
    """
    Resets all auto posters. Removing the old ones and adding the new ones.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    """
    for guild in SLASH_CLIENT.guilds:
        for channel in chain(guild.channels.values(), guild.threads.values()):
            reset_channel(client, channel)


def reset_channel(client, channel):
    """
    Resets the given channel of auto posting.
    
    Parameters
    ----------
    client : ``Client``
        The client who would post.
    channel : ``Channel``
        The channel to reset.
    """
    if should_auto_post_in_channel(client, channel):
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
    reset_auto_posters(SLASH_CLIENT)


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
