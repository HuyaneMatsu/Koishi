import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_available_balance


def _iter_options():
    yield (
        2000,
        3000,
        Embed(
            'Insufficient available balance',
            (
                f'You have 2000 available {EMOJI__HEART_CURRENCY} '
                f'which is lower than 3000 {EMOJI__HEART_CURRENCY}.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_available_balance(available_balance, investment):
    """
    Tests whether ``build_failure_embed_insufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    available_balance : `int`
        Available balance.
    
    investment : `int`
        The amount of balance to propose with.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_available_balance(available_balance, investment)
    vampytest.assert_instance(output, Embed)
    return output
