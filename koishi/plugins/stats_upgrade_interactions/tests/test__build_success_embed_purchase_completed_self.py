import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...balance_rendering.constants import COLOR_CODE_RED, COLOR_CODE_RESET

from ..embed_builders import build_success_embed_purchase_completed_self


def _iter_options():
    yield (
        2000,
        1000,
        2,
        13,
        Embed(
            'Purchase successful',
            f'You upgraded your bedroom skills to 13.',
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'2000 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 1000\n'
                f'```'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_purchase_completed_self(
    balance_before, required_balance, stat_index, stat_value_after
):
    """
    Tests whether ``build_success_embed_purchase_completed_self`` works as intended.
    
    Parameters
    ----------
    balance_before : `int`
        The user's balance before its purchase.
    
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    stat_value : `str`
        The stats current value.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_purchase_completed_self(
        balance_before, required_balance, stat_index, stat_value_after
    )
    vampytest.assert_instance(output, Embed)
    return output
