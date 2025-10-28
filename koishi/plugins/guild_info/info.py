__all__ = ('get_guild_info_response', )

from hata import Embed, ICON_TYPE_NONE, StringSelectOption, create_string_select
from hata.ext.slash import InteractionResponse, abort

from ...bots import FEATURE_CLIENTS

from .constants import (
    GUILD_INFO_FIELD_ALL, GUILD_INFO_FIELD_BOOSTERS, GUILD_INFO_FIELD_COUNTS, GUILD_INFO_FIELD_DEFAULT,
    GUILD_INFO_FIELD_EMOJIS, GUILD_INFO_FIELD_STICKERS, GUILD_INFO_SELECT_CUSTOM_ID
)
from .helpers import (
    add_guild_all_field, add_guild_boosters_field, add_guild_counts_field, add_guild_emojis_field, add_guild_info_field,
    add_guild_stickers_field
)


GUILD_FIELDS = {
    GUILD_INFO_FIELD_DEFAULT  : add_guild_info_field     ,
    GUILD_INFO_FIELD_COUNTS   : add_guild_counts_field   ,
    GUILD_INFO_FIELD_EMOJIS   : add_guild_emojis_field   ,
    GUILD_INFO_FIELD_STICKERS : add_guild_stickers_field ,
    GUILD_INFO_FIELD_BOOSTERS : add_guild_boosters_field ,
    GUILD_INFO_FIELD_ALL      : add_guild_all_field      ,
}


GUILD_INFO_SELECT = create_string_select(
    [StringSelectOption(value) for value in sorted(GUILD_FIELDS.keys())],
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


@FEATURE_CLIENTS.interactions(custom_id = GUILD_INFO_SELECT_CUSTOM_ID)
async def guild_info_component_command(client, event, *, values):
    """
    Handles a guild info select interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received event.
    
    values : `None | tuple<str>`
        the selected value.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    if values is None:
        return
    
    return await get_guild_info_response(client, event, values[0])
