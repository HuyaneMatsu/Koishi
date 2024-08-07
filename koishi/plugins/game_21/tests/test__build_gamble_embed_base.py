import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..constants import ACE_INDEX, CARD_NUMBERS, CARD_TYPES
from ..hand import Hand
from ..rendering import build_gamble_embed_base


def _iter_options():
    hand = Hand()
    hand.add_card(len(CARD_NUMBERS) + 8)
    hand.add_card(ACE_INDEX)
    
    yield(
        hand,
        'Hey mister',
        Embed(
            'Hey mister',
            f'You have cards equal to {hand.total} weight at your hand.',
            color = COLOR__GAMBLING,
        ).add_field(
            'Round 1',
            f'You pulled {CARD_TYPES[1]} {CARD_NUMBERS[8]}',
        ).add_field(
            'Round 2',
            f'You pulled {CARD_TYPES[0]} {CARD_NUMBERS[ACE_INDEX]}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_gamble_embed_base(hand, title):
    """
    Tests whether ``build_gamble_embed_base`` works as intended.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    title : `str`
        The title to add.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_gamble_embed_base(hand, title)
    vampytest.assert_instance(output, Embed)
    return output
