__all__ = ()

from hata import Embed, ICON_TYPE_NONE
from hata.ext.slash import InteractionResponse, Option, StringSelect, abort

from ...bots import FEATURE_CLIENTS

from .base_command import GUILD_COMMANDS
from .info_helpers import (
    add_guild_all_field, add_guild_boosters_field, add_guild_counts_field, add_guild_emojis_field, add_guild_info_field,
    add_guild_stickers_field
)


GUILD_INFO_SELECT_CUSTOM_ID = 'guild.info.select'

DEFAULT_GUILD_FIELD = 'info'

GUILD_FIELDS = {
    DEFAULT_GUILD_FIELD : add_guild_info_field     ,
    'counts'            : add_guild_counts_field   ,
    'emojis'            : add_guild_emojis_field   ,
    'stickers'          : add_guild_stickers_field ,
    'boosters'          : add_guild_boosters_field ,
    'all'               : add_guild_all_field      ,
}

GUILD_INFO_SELECT = StringSelect(
    [Option(value) for value in sorted(GUILD_FIELDS.keys())],
    custom_id = GUILD_INFO_SELECT_CUSTOM_ID,
    placeholder = 'Select an other field!',
)


async def get_guild_info_response(client, event, field):
    """
    Gets a guild info response for the given field.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    field : `str`
        The field's name to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    guild = event.guild
    if (guild is None) or guild.partial:
        abort('I must be in the guild to execute this command.')
    
    embed = Embed(
        guild.name,
        color = (guild.icon_hash & 0xffffff if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xffffff),
    ).add_thumbnail(
        guild.icon_url_as(size = 128),
    )
    
    await GUILD_FIELDS[field](client, guild, embed, True)
    
    return InteractionResponse(
        embed = embed,
        components = GUILD_INFO_SELECT,
    )


@GUILD_COMMANDS.interactions(name = 'info')
async def guild_info_slash_command(
    client,
    event,
    field: ([*GUILD_FIELDS.keys()], 'Which fields should I show?') = DEFAULT_GUILD_FIELD,
):
    """
    Shows some information about the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    field : `str` = `DEFAULT_GUILD_FIELD`, Optional
        The field's name to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return await get_guild_info_response(client, event, field)


@FEATURE_CLIENTS.interactions(custom_id = GUILD_INFO_SELECT_CUSTOM_ID)
async def guild_info_component_command(client, event):
    """
    Handles a guild info select interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    if event.message.interaction.user is not event.user:
        return
    
    values = event.values
    if values is None:
        return
    
    return await get_guild_info_response(client, event, values[0])
