__all__ = ()

from hata import create_section, create_separator, create_text_display, create_thumbnail_media

from .content_building import produce_equipped_item_description


def build_user_equipment_components(user, user_stats, guild_id):
    """
    Builds user equipment components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The stats.
    
    user_stats : ``UserStats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    components : ``list<Component>>`
    """
    components = []
    
    # Header
    
    components.append(create_section(
        create_text_display(f'# {user.name_at(guild_id)}\'s equipment'),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    components.append(create_separator())
    
    # Equipment
    stats_calculated = user_stats.stats_calculated
    
    components.append(create_text_display(
        ''.join([*produce_equipped_item_description('Species', stats_calculated.item_species, None, 'Neet')])
    ))
    components.append(create_separator())
    
    components.append(create_text_display(
        ''.join([*produce_equipped_item_description('Costume', stats_calculated.item_costume, None, 'Tracksuit')])
    ))
    components.append(create_separator())
    
    components.append(create_text_display(
        ''.join([*produce_equipped_item_description('Head accessory', stats_calculated.item_head, None, 'Hairband')])
    ))
    components.append(create_separator())
    
    components.append(create_text_display(
        ''.join([*produce_equipped_item_description('Weapon', stats_calculated.item_weapon, None, 'Bare hands')])
    ))
    
    return components
