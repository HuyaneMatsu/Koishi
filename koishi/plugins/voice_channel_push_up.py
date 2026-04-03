__all__ = ()

from hata import Guild, Channel, CHANNELS, KOKORO
from scarletio import Lock, Task

from ..bots import MAIN_CLIENT

# Only registered into the main client.

GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)
CATEGORY__VOICE = Channel.precreate(914407653114011648)
CATEGORY__RADIO = Channel.precreate(1016357856540373102)
CHANNEL__EXCEPTION = Channel.precreate(1007940975861182507)

PULL_DOWN_HANDLES = {}
PULL_DOWN_TIMEOUT = 60.0

MOVE_LOCK = Lock(KOKORO)
MOVABLE_PARENT_IDS = {0, CATEGORY__VOICE.id, CATEGORY__RADIO.id}


def should_channel_be_pushed_up(channel):
    """
    Returns whether the given channel of the id should be pushed up.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    
    Returns
    -------
    should_channel_be_pushed_up : `bool`
    """
    channel_id = channel.id
    
    user_count = 0
    
    for voice_state in GUILD__KOISHI_CLAN.iter_voice_states():
        if voice_state.channel_id != channel_id:
            continue
        
        if voice_state.user.bot:
            continue
        
        if voice_state.self_stream:
            return True
        
        user_count += 1
        continue
    
    if user_count >= 2:
        return True
    
    return False


def should_process_action_in_channel(channel):
    """
    Returns whether the action at the given channel should be processed.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to check.
    
    Returns
    -------
    should_process_action_in_channel : `bool`
    """
    if channel is CHANNEL__EXCEPTION:
        return False
    
    if not channel.is_guild_voice():
        return False
    
    if channel.parent_id in MOVABLE_PARENT_IDS:
        return True
    
    return False


async def update_channel_push_up( channel):
    """
    Updates the channel's push up state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel which states to update.
    """
    async with MOVE_LOCK:
        if should_channel_be_pushed_up(channel):
            if channel.parent_id:
                try:
                    handle = PULL_DOWN_HANDLES[channel.id]
                except KeyError:
                    pass
                else:
                    handle.cancel()
                
                await MAIN_CLIENT.channel_edit(channel, position = 0, parent_id = 0)
        
        else:
            if (not channel.parent_id) and (channel.id not in PULL_DOWN_HANDLES):
                PULL_DOWN_HANDLES[channel.id] = KOKORO.call_after(PULL_DOWN_TIMEOUT, invoke_pull_down, channel)


def invoke_pull_down(channel):
    """
    Invokes the pull down action.
    
    Called after pull down timeout occurred.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to pull down.
    """
    try:
        del PULL_DOWN_HANDLES[channel.id]
    except KeyError:
        pass
    
    Task(KOKORO, pull_down(channel))


async def pull_down(channel):
    """
    Pulls down the given channel.
    
    This function is a coroutine.
    Parameters
    ----------
    channel : ``Channel``
        The channel to pull down.
    """
    if 'radio' in channel.name.casefold():
        target_category = CATEGORY__RADIO
    else:
        target_category = CATEGORY__VOICE
    
    await MAIN_CLIENT.channel_edit(channel, position = 0, parent_id = target_category)


@MAIN_CLIENT.events
async def ready(client):
    """
    Handles a ready event of the client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    client.events.remove(ready)
    
    for channel in GUILD__KOISHI_CLAN.channels.values():
        if should_process_action_in_channel(channel):
            await update_channel_push_up(channel)


@MAIN_CLIENT.events
async def user_voice_join(client, voice_state):
    """
    Handles a user voice channel join event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The voice state of the joining user.
    """
    if voice_state.guild_id != GUILD__KOISHI_CLAN.id:
        return
    
    try:
        channel = CHANNELS[voice_state.channel_id]
    except KeyError:
        return
    
    if should_process_action_in_channel(channel):
        await update_channel_push_up(channel)


@MAIN_CLIENT.events
async def user_voice_move(client, voice_state, channel_id):
    """
    Handles a user voice move event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The voice state of the moving user.
    channel_id : `int`
        The channel's identifier that the user left.
    """
    if voice_state.guild_id != GUILD__KOISHI_CLAN.id:
        return
    
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        pass
    else:
        if should_process_action_in_channel(channel):
            await update_channel_push_up(channel)
    
    try:
        channel = CHANNELS[voice_state.channel_id]
    except KeyError:
        pass
    else:
        if should_process_action_in_channel(channel):
            await update_channel_push_up(channel)


@MAIN_CLIENT.events
async def user_voice_leave(client, voice_state, channel_id):
    """
    Handles a user voice channel leave event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The voice state of the user.
    channel_id : `int`
        The channel's identifier that the user left.
    """
    if voice_state.guild_id != GUILD__KOISHI_CLAN.id:
        return
    
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        return
    
    if should_process_action_in_channel(channel):
        await update_channel_push_up(channel)


@MAIN_CLIENT.events
async def user_voice_update(client, voice_state, old_attributes):
    """
    Handles a user voice state update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The voice state of the user.
    old_attributes : `dict<str, object>`
        The voice state's old attributes that changed.
    """
    if voice_state.guild_id != GUILD__KOISHI_CLAN.id:
        return
    
    try:
        channel = CHANNELS[voice_state.channel_id]
    except KeyError:
        return
    
    if should_process_action_in_channel(channel):
        await update_channel_push_up(channel)


def teardown(module):
    """
    Called when the plugin is being unloaded.
    
    Parameters
    ----------
    module : `ModuleType`
        This file.
    """
    for handle in PULL_DOWN_HANDLES.values():
        handle.cancel()
    
    PULL_DOWN_HANDLES.clear()


async def setup(module):
    """
    Called when the plugin is being loaded.
    
    Parameters
    ----------
    module : `ModuleType`
        This file.
    """
    for channel in GUILD__KOISHI_CLAN.channels.values():
        if should_process_action_in_channel(channel):
            await update_channel_push_up(channel)
