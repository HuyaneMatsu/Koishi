__all__ = ()

from os.path import dirname as get_directory_name, join as join_paths

from hata import Client, Embed, LocalAudio

from ...bots import MAIN_CLIENT


PARANOIA_TITLE = 'Pa-Pa-Pa-Pa-Paranoia'
PARANOIA_URL = 'https://www.youtube.com/watch?v=wnli28pjsn4'
PARANOIA_IMAGE_URL = (
    'https://i.ytimg.com/vi/wnli28pjsn4/hqdefault.jpg?'
    'sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLC27YDJ7qBQhLzq7y5iD85vlIYuHw'
)
PARANOIA_COLOR = 0x9f80ad

SADISTIC_PARANOIA_TITLE = 'Sadistic Paranoia'
SADISTIC_PARANOIA_URL = 'https://www.youtube.com/watch?v=ZjFIt78fCxI'
SADISTIC_PARANOIA_IMAGE_URL = (
    'https://i.ytimg.com/vi/ZjFIt78fCxI/hqdefault.jpg?'
    'sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD_5vyQPYLiT5-NXbZ-JkHPfX72Xw'
)
SADISTIC_PARANOIA_COLOR = 0x08963c


DIRECTORY_PATH = get_directory_name(__spec__.origin)
PARANOIA_PATH = join_paths(DIRECTORY_PATH, 'assets', 'Paranoia.mp3')
SADISTIC_PARANOIA_PATH = join_paths(DIRECTORY_PATH, 'assets', 'Sadistic Paranoia.mp3')


def is_name_satori(name):
    """
    Returns whether `satori` is in the given `name`.
    
    Parameters
    ----------
    name : `str`
        The name to check.
    
    Returns
    -------
    is_name_satori : `bool`
    """
    name = name.casefold()
    if 'satori' in name:
        return True
    
    if 'さとり' in name:
        return True
    
    return False


def is_event_user_satori(event):
    """
    Returns whether the event's user has `satori` in it's name (or nick).
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The event to check.
    
    Returns
    -------
    is_event_user_satori : `bool`
    """
    user = event.user
    user_name = user.name
    
    user_is_satori = is_name_satori(user_name)
    if user_is_satori:
        return user_is_satori
    
    user_nick = user.name_at(event.guild_id)
    if (user_name is user_nick):
        return False
    
    return is_name_satori(user_nick)


def build_response_embed(user_is_satori):
    """
    Builds a response embed of the `paranoia` command.
    
    Parameters
    ----------
    user_is_satori : `bool`
        Whether satori embed should be built.
    
    Returns
    -------
    embed : ``Embed``
    """
    if user_is_satori:
        title = SADISTIC_PARANOIA_TITLE
        color = PARANOIA_COLOR
        url = SADISTIC_PARANOIA_URL
        image_url = SADISTIC_PARANOIA_IMAGE_URL
    else:
        title = PARANOIA_TITLE
        color = SADISTIC_PARANOIA_COLOR
        url = PARANOIA_URL
        image_url = PARANOIA_IMAGE_URL
    
    return Embed(
        title,
        color = color,
        url = url,
    ).add_image(
        image_url,
    )


async def disconnect_voice_client_after_playing(voice_client, last_source):
    """
    Disconnects the voice client after playing an audio.
    
    This function is a coroutine.
    
    Parameters
    ----------
    self : ``VoiceClient``
        The respective voice client.
    last_source : `None`, ``AudioSource``
        The audio that was played.
    """
    await voice_client.disconnect()


async def try_play_paranoia(client, event, user_is_satori):
    """
    Tries to play paranoia if the user is in a voice channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    """
    guild = event.guild
    if guild is None:
        return
    
    if guild.id in client.voice_clients:
        return
    
    try:
        voice_state = guild.voice_states[event.user.id]
    except KeyError:
        return
    
    if voice_state.deaf or voice_state.self_deaf:
        return
    
    voice_channel = voice_state.channel
    if (voice_channel is None):
        return
    
    if not voice_channel.cached_permissions_for(client).can_connect:
        return
    
    voice_client = await client.join_voice(voice_channel)
    voice_client.call_after = disconnect_voice_client_after_playing
    
    if voice_channel.is_guild_stage():
        await voice_client.join_speakers()
    
    if user_is_satori:
        audio_path = SADISTIC_PARANOIA_PATH
    else:
        audio_path = PARANOIA_PATH
    
    source = await LocalAudio(audio_path)
    
    voice_client.append(source)


@MAIN_CLIENT.interactions(is_global = True)
async def paranoia(client, event):
    """Pa-Pa-Pa-Pa-Paranoia!!!"""
    user_is_satori = is_event_user_satori(event)
    yield build_response_embed(user_is_satori)
    await try_play_paranoia(client, event, user_is_satori)
