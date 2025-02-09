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
                f'Are you sure you want to hire ninjas to locate and burn your 3rd divorce papers for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_purchase_confirmation_self(required_balance, relationship_divorce_count):
    """
    Tests whether ``build_question_embed_purchase_confirmation_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_question_embed_purchase_confirmation_self(required_balance, relationship_divorce_count)
    vampytest.assert_instance(output, Embed)
    return output
