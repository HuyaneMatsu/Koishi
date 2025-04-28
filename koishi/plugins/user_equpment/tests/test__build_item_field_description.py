import vampytest
from hata import BUILTIN_EMOJIS

from ...item_modifier_core import (
    MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT, Modifier, construct_modifier_type
)

from ..embed_builders import _build_item_field_description, EMPTY_UNICODE


def _iter_options():
    emoji = BUILTIN_EMOJIS['heart']
    
    yield (
        None,
        'Fiery Sea',
        None,
        3,
        (
            f'Fiery Sea\n'
            f'```\n'
            f'{EMPTY_UNICODE}\n'
            f'{EMPTY_UNICODE}\n'
            f'{EMPTY_UNICODE}\n'
            f'```'
        )
    )
    
    yield (
        emoji,
        'Fiery Sea',
        (
            Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), 2),
            Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), -4),
            Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), 10)
        ),
        3,
        (
            f'{emoji} Fiery Sea\n'
            f'```\n'
            f'+2 Fishing\n'
            f'-4 Fishing\n'
            f'+10% Fishing\n'
            f'```'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_item_field_description(item_emoji, item_name, item_modifiers, modifiers_adjustment_to):
    """
    Tests whether ``_build_item_field_description`` works as intended.
    
    Parameters
    ----------
    item_emoji : ``None | Emoji``
        The emoji of the item.
    
    item_name : `str`
        The item's name.
    
    item_modifiers : `None | tuple<Modifier>`
        Item modifiers.
    
    modifiers_adjustment_to : `int`
        The amount of modifiers to expand the modifier list to.
    
    Returns
    -------
    output : `str`
    """
    output = _build_item_field_description(item_emoji, item_name, item_modifiers, modifiers_adjustment_to)
    vampytest.assert_instance(output, str)
    return output
