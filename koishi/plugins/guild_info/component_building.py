__all__ = ()

from hata import (
    StringSelectOption, create_row, create_section, create_separator, create_string_select, create_text_display,
    create_thumbnail_media
)

from .constants import (
    GUILD_INFO_FLAGS, GUILD_INFO_FLAG_BOOSTERS, GUILD_INFO_FLAG_BOOST_PERKS, GUILD_INFO_FLAG_COUNTS,
    GUILD_INFO_FLAG_EMOJIS, GUILD_INFO_FLAG_EVEN_IF_EMPTY, GUILD_INFO_FLAG_INFO, GUILD_INFO_FLAG_STICKERS,
    GUILD_INFO_SELECT_CUSTOM_ID
)
from .content_building import (
    produce_guild_boost_perks_description, produce_guild_boosters_description, produce_guild_counts_description,
    produce_guild_emojis_description, produce_guild_info_description, produce_guild_stickers_description
)


def build_guild_info_components(guild, guild_info_flags):
    """
    Builds guild info components.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to builds components for.
    
    guild_info_flags : `int`
        Flags describing what to render.
    
    Returns
    -------
    components : ``list<Component>``
    """
    # build content components
    contents = []
    even_if_empty = True if guild_info_flags & GUILD_INFO_FLAG_EVEN_IF_EMPTY else False
    
    for flag, producer in (
        (GUILD_INFO_FLAG_INFO, produce_guild_info_description),
        (GUILD_INFO_FLAG_COUNTS, produce_guild_counts_description),
        (GUILD_INFO_FLAG_EMOJIS, produce_guild_emojis_description),
        (GUILD_INFO_FLAG_STICKERS, produce_guild_stickers_description),
        (GUILD_INFO_FLAG_BOOST_PERKS, produce_guild_boost_perks_description),
        (GUILD_INFO_FLAG_BOOSTERS, produce_guild_boosters_description),
    ):
        if guild_info_flags & flag:
            content = ''.join([*producer(guild, even_if_empty)])
            if content:
                contents.append(content)
    
    
    components = []
    
    # Header
    title_component = create_text_display(f'# {guild.name}')
    
    thumbnail_url = guild.icon_url_as(size = 128)
    if thumbnail_url is None:
        header_component = title_component
    else:
        header_component = create_section(
            title_component,
            create_text_display(contents.pop(0) if contents else '*nothing to display*'),
            thumbnail = create_thumbnail_media(thumbnail_url),
        )
    
    components.append(header_component)
    
    # Description
    
    for content in contents:
        components.append(create_separator())
        components.append(create_text_display(content))
    
    # Control
    components.append(create_separator())
    components.append(create_row(create_string_select(
        [StringSelectOption(format(flag, 'x'), name) for name, flag in GUILD_INFO_FLAGS],
        custom_id = GUILD_INFO_SELECT_CUSTOM_ID,
        placeholder = 'Select an other field!',
    )))
    
    return components
