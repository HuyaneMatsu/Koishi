__all__ = ()

from hata import (
    create_button, create_media_gallery, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from .chart import get_user_stats_chart_color, get_user_stats_chart_url
from .content_building import produce_user_stats_primary_description, produce_user_stats_secondary_description
from .custom_ids import CUSTOM_ID_USER_STATS_PRIMARY_BUILDER, CUSTOM_ID_USER_STATS_SECONDARY_BUILDER


def build_user_stats_primary_components(user_id, target_user, user_stats, guild_id):
    """
    Builds user stats primary components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    target_user : ``ClientUserBase``
        The user who's stats are shown.
    
    user_stats : ``UserStats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header & Description
    # We merge them, so we get better rendering.
    
    components.append(
        create_section(
            create_text_display(f'# {target_user.name_at(guild_id)}\'s stats'),
            create_text_display(''.join([*produce_user_stats_primary_description(user_stats)])),
            thumbnail = create_thumbnail_media(target_user.avatar_url_at(guild_id))
        ),
    )
    components.append(create_separator())
    
    # Chart
    components.append(
        create_media_gallery(
            get_user_stats_chart_url(user_stats, get_user_stats_chart_color(user_stats)),
        ),
    )
    components.append(create_separator())
    
    # Control
    
    components.append(create_row(
        create_button(
            'View secondary stats & skills',
            custom_id = CUSTOM_ID_USER_STATS_SECONDARY_BUILDER(user_id, target_user.id),
        ),
    ))
    
    return components


def build_user_stats_secondary_components(user_id, target_user, user_stats, guild_id):
    """
    Builds user stats secondary components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    target_user : ``ClientUserBase``
        The user who's stats are shown.
    
    user_stats : ``UserStats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header & Description
    # We merge them, so we get better rendering.
    
    components.append(
        create_section(
            create_text_display(f'# {target_user.name_at(guild_id)}\'s secondary stats & skills'),
            create_text_display(''.join([*produce_user_stats_secondary_description(user_stats)])),
            thumbnail = create_thumbnail_media(target_user.avatar_url_at(guild_id))
        ),
    )
    components.append(create_separator())
    
    # Control
    
    components.append(create_row(
        create_button(
            'View primary stats',
            custom_id = CUSTOM_ID_USER_STATS_PRIMARY_BUILDER(user_id, target_user.id),
        ),
    ))
    
    return components
