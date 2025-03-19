import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_question_embed_purchase_confirmation_self


def _iter_options():
    yield (
        2000,
        2,
        12,
        Embed(
            'Stat upgrade',
            (
                f'Are you sure to upgrade your bedroom skills to 12 for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            )
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_purchase_confirmation_self(
    required_balance, stat_index, stat_value_after
):
    """
    Tests whether ``build_question_embed_purchase_confirmation_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_question_embed_purchase_confirmation_self(
        required_balance, stat_index, stat_value_after
    )
    vampytest.assert_instance(output, Embed)
    return output
