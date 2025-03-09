import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_available_balance


def _iter_options():
    yield (
        100,
        200,
        Embed(
            'Insufficient available balance',
            (
                f'You cannot bet 200 {EMOJI__HEART_CURRENCY}, '
                f'you have only 100 {EMOJI__HEART_CURRENCY} available.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_available_balance(available_balance, bet_amount):
    """
    Tests whether ``build_failure_embed_insufficient_available_balance`` works as intend.
    
    Parameters
    ----------
    available_balance : `int`
        The available balance of the user.
    
    bet_amount : `int`
        The amount the user bet.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_available_balance(available_balance, bet_amount)
    vampytest.assert_instance(output, Embed)
    return output
