import vampytest

from ..constants import ACE_INDEX, CARD_NUMBERS, CARD_TYPES
from ..hand import Hand
from ..rendering import build_done_field_description


def _iter_options():
    hand = Hand()
    
    yield (
        hand,
        '_ _',
    )
    
    hand = Hand()
    hand.add_card(len(CARD_NUMBERS) + 8)
    hand.add_card(ACE_INDEX)
    
    
    yield(
        hand,
        (
            f'Round 1: {CARD_TYPES[1]} {CARD_NUMBERS[8]}\n'
            f'Round 2: {CARD_TYPES[0]} {CARD_NUMBERS[ACE_INDEX]}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_done_field_description(hand):
    """
    Tests whether ``build_done_field_description`` works as intended.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to create done description for.
    
    Returns
    -------
    output : `str`
    """
    output = build_done_field_description(hand)
    vampytest.assert_instance(output, str)
    return output
