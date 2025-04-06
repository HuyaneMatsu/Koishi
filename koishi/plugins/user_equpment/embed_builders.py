__all__ = ('build_equipment_embed',)

from hata import Embed

from ..item_modifier_core import get_modifier_name_and_amount_postfix


EMPTY_UNICODE = '\u200b'


def _add_items_row(
    embed,
    item_left,
    item_left_slot_name,
    item_left_emoji_default,
    item_left_name_default,
    item_right,
    item_right_slot_name,
    item_right_emoji_default,
    item_right_name_default,
):
    """
    Adds an item row of 2 items to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        Embed to extend.
    
    item_left : `None | Item`
        Left item to render.
    
    item_left_slot_name : `str`
        Left item slot name.
    
    item_left_emoji_default : `None | Emoji`
        Left item's default emoji to use.
    
    item_left_name_default : `str`
        Left item's default name.
    
    item_right : `None | Item`
        Left item to render.
    
    item_right_slot_name : `str`
        Left item slot name.
    
    item_right_emoji_default : `None | Emoji`
        Left item's default emoji to use.
    
    item_right_name_default : `str`
        Left item's default name.
    """
    if item_left is None:
        item_left_emoji = item_left_emoji_default
        item_left_name = item_left_name_default
        item_left_modifiers = None
        
    else:
        item_left_emoji = item_left.emoji
        item_left_name = item_left.name
        item_left_modifiers = item_left.modifiers
    
    item_left_modifier_count = 0 if item_left_modifiers is None else len(item_left_modifiers)
    
    
    if item_right is None:
        item_right_emoji = item_right_emoji_default
        item_right_name = item_right_name_default
        item_right_modifiers = None
        
    else:
        item_right_emoji = item_right.emoji
        item_right_name = item_right.name
        item_right_modifiers = item_right.modifiers
    
    item_right_modifier_count = 0 if item_right_modifiers is None else len(item_right_modifiers)
    
    modifiers_adjustment_to = max(item_left_modifier_count, item_right_modifier_count, 1)
    
    embed.add_field(
        item_left_slot_name,
        _build_item_field_description(item_left_emoji, item_left_name, item_left_modifiers, modifiers_adjustment_to),
        True,
    )
    embed.add_field(
        item_right_slot_name,
        _build_item_field_description(item_right_emoji, item_right_name, item_right_modifiers, modifiers_adjustment_to),
        True,
    )


def _build_item_field_description(item_emoji, item_name, item_modifiers, modifiers_adjustment_to):
    """
    Builds an item field's description.
    
    Parameters
    ----------
    item_emoji : `None | Emoji`
        The emoji of the item.
    
    item_name : `str`
        The item's name.
    
    item_modifiers : `None | tuple<Modifier>`
        Item modifiers.
    
    modifiers_adjustment_to : `int`
        The amount of modifiers to expand the modifier list to.
    
    Returns
    -------
    description : `str`
    """
    description_parts = []
    
    if (item_emoji is not None):
        description_parts.append(item_emoji.as_emoji)
        description_parts.append(' ')
    
    description_parts.append(item_name)
    
    description_parts.append('\n```\n')
    
    if (item_modifiers is not None):
        for modifier in item_modifiers:
            name, postfix = get_modifier_name_and_amount_postfix(modifier.type)
            amount = modifier.amount
            description_parts.append('+' if amount >= 0 else '-')
            description_parts.append(str(abs(amount)))
            if (postfix is not None):
                description_parts.append(postfix)
            description_parts.append(' ')
            description_parts.append(name)
            description_parts.append('\n')
        
        modifiers_adjustment_to -= len(item_modifiers)
    
    while modifiers_adjustment_to > 0:
        modifiers_adjustment_to -= 1
        description_parts.append(EMPTY_UNICODE)
        description_parts.append('\n')
    
    description_parts.append('```')
    return ''.join(description_parts)


def build_equipment_embed(user, stats, guild_id):
    """
    Builds an embed showing the user's equipments.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The stats.
    
    stats : ``Stats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    stats_calculated = stats.stats_calculated
    
    embed = Embed(f'{user.name_at(guild_id)}\'s equipment').add_thumbnail(user.avatar_url_at(guild_id))
    
    _add_items_row(
        embed,
        stats_calculated.item_species,
        'Species',
        None,
        'Neet',
        stats_calculated.item_costume,
        'Costume',
        None,
        'Tracksuit',
    )
    
    embed.add_field(EMPTY_UNICODE, EMPTY_UNICODE)
    
    _add_items_row(
        embed,
        stats_calculated.item_head,
        'Head accessory',
        None,
        'Hairband',
        stats_calculated.item_weapon,
        'Weapon',
        None,
        'Bare hands',
    )
    
    return embed
