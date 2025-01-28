import vampytest
from hata import Embed

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_balance_self


def _iter_options():
    yield (
        2000,
        3,
        Embed(
            'Insufficient balance',
            (
                'You do not have enough available heart to buy more relationship slots.\n'
                f'You need 2000 {EMOJI__HEART_CURRENCY} to buy the 3rd slot.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_balance_self(required_balance, new_relationship_slot_count):
    """
    Tests whether ``build_failure_embed_insufficient_balance_self`` works as intended.
    
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
    output = build_failure_embed_insufficient_balance_self(required_balance, new_relationship_slot_count)
    vampytest.assert_instance(output, Embed)
    return output
