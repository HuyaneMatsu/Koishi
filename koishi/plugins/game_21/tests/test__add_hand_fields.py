import vampytest
from hata import Embed

from ..constants import ACE_INDEX, CARD_NUMBERS, CARD_TYPES
from ..hand import Hand
from ..rendering import add_hand_fields


def _iter_options():
    hand = Hand()
    hand.add_card(len(CARD_NUMBERS) + 8)
    hand.add_card(ACE_INDEX)
    
    yield(
        Embed(),
        hand,
        Embed().add_field(
            'Round 1',
            f'You pulled {CARD_TYPES[1]} {CARD_NUMBERS[8]}',
        ).add_field(
            'Round 2',
            f'You pulled {CARD_TYPES[0]} {CARD_NUMBERS[ACE_INDEX]}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_hand_fields(embed, hand):
    """
    Tests whether ``add_hand_fields`` works as intended.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    hand : ``Hand``
        The hand to add.
    
    Returns
    -------
    output : ``Embed``
    """
    output = add_hand_fields(embed, hand)
    vampytest.assert_instance(output, Embed)
    return output
