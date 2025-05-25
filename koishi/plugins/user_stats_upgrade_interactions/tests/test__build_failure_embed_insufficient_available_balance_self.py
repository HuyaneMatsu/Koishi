import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_available_balance_self


def _iter_options():
    yield (
        2000,
        1000,
        2,
        12,
        Embed(
            'Insufficient available balance',
            (
                f'You cannot upgrade your bedroom skills to 12 because you have only '
                f'1000 available {EMOJI__HEART_CURRENCY} which is lower than the required '
                f'2000 {EMOJI__HEART_CURRENCY}.'
            )
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_available_balance_self(
    required_balance, available_balance, stat_index, stat_value_after
):
    """
    Tests whether ``build_failure_embed_insufficient_available_balance_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_available_balance_self(
        required_balance, available_balance, stat_index, stat_value_after
    )
    vampytest.assert_instance(output, Embed)
    return output
