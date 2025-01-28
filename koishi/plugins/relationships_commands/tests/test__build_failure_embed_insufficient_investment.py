import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_investment


def _iter_options():
    yield (
        2000,
        3000,
        Embed(
            'Insufficient investment',
            (
                f'Your investment 3000 {EMOJI__HEART_CURRENCY} is lower than the required '
                f'2000 {EMOJI__HEART_CURRENCY}.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_investment(relationship_cost, investment):
    """
    Tests whether ``build_failure_embed_insufficient_investment`` works as intended.
    
    Parameters
    ----------
    relationship_cost : `int`
        The required balance to engage the relationship with.
    
    investment : `int`
        The amount of balance to propose with.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_investment(relationship_cost, investment)
    vampytest.assert_instance(output, Embed)
    return output
