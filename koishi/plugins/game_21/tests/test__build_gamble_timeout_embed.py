import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY, COLOR__GAMBLING

from ..constants import ACE_INDEX, CARD_NUMBERS, CARD_TYPES
from ..hand import Hand
from ..rendering import build_gamble_timeout_embed


def _iter_options():
    hand = Hand()
    hand.add_card(len(CARD_NUMBERS) + 8)
    hand.add_card(ACE_INDEX)
    
    yield(
        hand,
        1000,
        Embed(
            f'Gambled {1000!s} {EMOJI__HEART_CURRENCY} and timed out',
            f'You have cards equal to {hand.total} weight at your hand.',
            color = COLOR__GAMBLING,
        ).add_field(
            'Round 1',
            f'You pulled {CARD_TYPES[1]} {CARD_NUMBERS[8]}',
        ).add_field(
            'Round 2',
            f'You pulled {CARD_TYPES[0]} {CARD_NUMBERS[ACE_INDEX]}',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_gamble_timeout_embed(hand, amount):
    """
    Tests whether ``build_gamble_timeout_embed`` works as intended.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    amount : `int`
        The gambled amount.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_gamble_timeout_embed(hand, amount)
    vampytest.assert_instance(output, Embed)
    return output
