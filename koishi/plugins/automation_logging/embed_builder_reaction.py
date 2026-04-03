__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import Embed, DATETIME_FORMAT_CODE, ReactionDeleteEvent

from .constants import COLOR_ADD, COLOR_DELETE
from .embed_builder_shared import get_preinstanced_repr

from ..rendering_helpers import build_user_with_guild_profile_description


def _build_location_description(channel):
    """
    Returns location description including `channel` representation and `.guild` representation.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to represent.
    
    Returns
    -------
    description : `str`
    """
    into = []
    into.append('Channel: ')
    into.append(channel.display_name)
    into.append(' (')
    into.append(str(channel.id))
    into.append(')\n')
    
    guild = channel.guild
    into.append('Guild: ')
    if guild is None:
        into.append('null')
    else:
        into.append(guild.name)
        into.append(' (')
        into.append(str(guild.id))
        into.append(')')
    
    return ''.join(into)


def _build_reaction_description(event):
    """
    Builds reaction description including `.type` and `.emoji`.
    Parameters
    ----------
    event : ``ReactionAddEvent``
        The reaction event to represent.
    
    Returns
    -------
    description : `str`
    """
    into = []
    into.append('Type: ')
    into.append(get_preinstanced_repr(event.type))
    into.append('\n')
    
    emoji = event.emoji
    
    into.append('Emoji: ')
    into.append(emoji.name)
    into.append(' (')
    into.append(str(emoji.id))
    into.append(')')
    
    return ''.join(into)


def build_reaction_event_embed(event):
    """
    Builds reaction event embed for both `add` and `delete` events.
    
    Parameters
    ----------
    event : ``ReactionAddEvent``
        The triggered event.
    addition : `bool`
        Whether the reaction was added or removed.
    
    Returns
    -------
    embed : ``Embed``
    """
    if isinstance(event, ReactionDeleteEvent):
        title = 'reaction deleted'
        color = COLOR_DELETE
    else:
        title = 'Reaction added'
        color = COLOR_ADD
    
    user = event.user
    message = event.message
    
    return Embed(
        user.full_name,
        build_user_with_guild_profile_description(user, user.get_guild_profile_for(message.guild_id)),
        color = color,
    ).add_author(
        title,
    ).add_field(
        'Location',
        _build_location_description(message.channel),
    ).add_field(
        'Reaction',
        _build_reaction_description(event),
    ).add_footer(
        format(DateTime.now(TimeZone.utc), DATETIME_FORMAT_CODE),
    ).add_thumbnail(
        user.avatar_url,
    )
