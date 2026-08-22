import vampytest
from hata import Component, create_button, create_row, create_text_display

from ..component_building import build_roll_response_components
from ..constants import EMOJI_REPEAT


def _iter_options():
    yield (
        2,
        6,
        0,
        0,
        [2, 4],
        6,
        [
            create_text_display(
                'Rolling 2d6\n'
                'Rolls: 2, 4\n'
                'Result: **6**'
            ),
            create_row(create_button(
                'Another',
                EMOJI_REPEAT,
                custom_id = f'roll.2.6.1.0.1.0',
            )),
        ],
    )
    
    yield (
        0,
        0,
        8,
        0,
        [],
        8,
        [
            create_text_display(
                'Rolling +8\n'
                'Result: **8**'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_roll_response_components(dice_count, dice_sides, fix_amount, luck, rolls, result):
    """
    Tests whether ``build_roll_response_components`` works as intended.
    
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
    output : ``list<Component>``
    """
    output = build_roll_response_components(dice_count, dice_sides, fix_amount, luck, rolls, result)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
