__all__ = ()

from hata import create_button, create_row, create_text_display

from .constants import EMOJI_REPEAT
from .content_building import produce_roll_description
from .custom_ids import CUSTOM_ID_ROLL_BUILDER


def build_roll_response_components(dice_count, dice_sides, fix_amount, luck, rolls, result):
    """
    Builds roll response components.
    
    Parameters
    ----------
    dice_count : `int`
        Amount of dices to roll.
    
    dice_sides : `int`
        How much sides each side have.
    
    fix_amount : `int`
        Added or subtracted amount.
    
    luck : `int`
        How lucky the user is.
    
    rolls : `list<int>`
        Rolls.
    
    result : `int`
        The sum of all rolls and the fix amount.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    
    components.append(create_text_display(
        ''.join([*produce_roll_description(dice_count, dice_sides, fix_amount, luck, rolls, result)])
    ))
    
    # Control
    
    if (dice_count and dice_sides):
        components.append(create_row(create_button(
            'Another',
            EMOJI_REPEAT,
            custom_id = CUSTOM_ID_ROLL_BUILDER(dice_count, dice_sides, fix_amount, luck),
        )))
    
    return components
