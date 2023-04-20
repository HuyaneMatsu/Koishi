__all__ = ()

from hata import Embed, ICON_TYPE_NONE
from hata.ext.slash import abort

from .info_helpers import (
    add_guild_all_field, add_guild_boosters_field, add_guild_counts_field, add_guild_emojis_field, add_guild_info_field,
    add_guild_stickers_field
)


DEFAULT_GUILD_FIELD = 'info'

GUILD_FIELDS = {
    DEFAULT_GUILD_FIELD : add_guild_info_field     ,
    'counts'            : add_guild_counts_field   ,
    'emojis'            : add_guild_emojis_field   ,
    'stickers'          : add_guild_stickers_field ,
    'boosters'          : add_guild_boosters_field ,
    'all'               : add_guild_all_field      ,
}


async def guild_info_command(client, event,
    field: ([*GUILD_FIELDS.keys()], 'Which fields should I show?') = DEFAULT_GUILD_FIELD,
):
    """Shows some information about the guild."""
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
    
    return embed
