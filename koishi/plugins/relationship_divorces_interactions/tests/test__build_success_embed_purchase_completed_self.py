import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed_purchase_completed_self


def _iter_options():
    yield (
        2000,
        3,
        Embed(
            'Purchase successful',
            (
                f'You sent out your hired ninjas to locate and burn your 3rd divorce papers for '
                f'2000 {EMOJI__HEART_CURRENCY}.\n'
                f'They completed the task splendid; the case is cool even in the summer.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_purchase_completed_self(required_balance, relationship_divorce_count):
    """
    Tests whether ``build_success_embed_purchase_completed_self`` works as intended.
    
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
    output = build_success_embed_purchase_completed_self(required_balance, relationship_divorce_count)
    vampytest.assert_instance(output, Embed)
    return output
