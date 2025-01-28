import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_question_embed_purchase_confirmation_self


def _iter_options():
    yield (
        2000,
        3,
        Embed(
            'Confirm your purchase',
            (
                f'Are you sure you want to buy your 3rd relationship slot for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_purchase_confirmation_self(required_balance, new_relationship_slot_count):
    """
    Tests whether ``build_question_embed_purchase_confirmation_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_question_embed_purchase_confirmation_self(required_balance, new_relationship_slot_count)
    vampytest.assert_instance(output, Embed)
    return output
