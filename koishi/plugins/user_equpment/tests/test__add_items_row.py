import vampytest
from hata import Embed

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..embed_builders import _add_items_row, EMPTY_UNICODE


def _iter_options():
    weapon = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        None,
        'Head accessory',
        None,
        'Hairband',
        
        weapon,
        'Weapon',
        None,
        'Bare hands',
        
        Embed().add_field(
            'Head accessory',
            (
                f'Hairband\n'
                f'```\n'
                f'{EMPTY_UNICODE}\n'
                f'{EMPTY_UNICODE}\n'
                f'{EMPTY_UNICODE}\n'
                f'{EMPTY_UNICODE}\n'
                f'```'
            ),
            True,
        ).add_field(
            'Weapon',
            (
                f'{weapon.emoji} Fishing rod\n'
                f'```\n'
                f'+1 Housewife capabilities\n'
                f'+1 Bedroom skills\n'
                f'+1 Loyalty\n'
                f'-2 Fishing\n'
                f'```'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_items_row(
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
    Tests whether ``_add_items_row`` works as intended.
    
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
    
    Returns
    -------
    output : ``Embed``
    """
    embed = Embed()
    _add_items_row(
        embed,
        item_left,
        item_left_slot_name,
        item_left_emoji_default,
        item_left_name_default,
        item_right,
        item_right_slot_name,
        item_right_emoji_default,
        item_right_name_default,
    )
    
    return embed
