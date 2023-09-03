__all__ = ()

from datetime import datetime as DateTime

from hata import DATETIME_FORMAT_CODE, Embed

from .embed_builder_shared import (
    maybe_add_modified_bool_field, maybe_add_modified_date_time_field, maybe_add_modified_flags_field,
    maybe_add_modified_icon_field, maybe_add_modified_nullable_string_field,
    maybe_add_modified_role_ids_difference_field
)


def build_guild_profile_update_embed(guild_profile, old_attributes):
    """
    Builds a guild profile update embed.
    
    Parameters
    ----------
    guild_profile : ``GuildProfile``
        The edited guild profile.
    old_attributes : `dict` of (`str`, `object`) items
        The emoji's old attributes that have been edited.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(f'Guild profile updated').add_footer(format(DateTime.utcnow(), DATETIME_FORMAT_CODE))
    
    maybe_add_modified_icon_field(embed, guild_profile, old_attributes, 'avatar', 'Avatar')
    maybe_add_modified_date_time_field(embed, guild_profile, old_attributes, 'boosts_since', 'Boosts since')
    maybe_add_modified_flags_field(embed, guild_profile, old_attributes, 'flags', 'Flags')
    maybe_add_modified_nullable_string_field(embed, guild_profile, old_attributes, 'nick', 'Nick')
    maybe_add_modified_bool_field(embed, guild_profile, old_attributes, 'pending', 'Pending')
    maybe_add_modified_role_ids_difference_field(embed, guild_profile, old_attributes, 'role_ids', 'Roles')
    maybe_add_modified_date_time_field(embed, guild_profile, old_attributes, 'timed_out_until', 'Timed out until')
    
    return embed
