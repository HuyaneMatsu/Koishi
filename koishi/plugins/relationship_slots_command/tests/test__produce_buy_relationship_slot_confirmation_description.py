import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_buy_relationship_slot_confirmation_description


def _iter_options():
    user = User.precreate(
        202511300011,
        name = 'Satori',
    )
    
    yield (
        5,
        6000,
        None,
        0,
        (
            f'Are you sure to buy the 5th relationship slot?\n'
            f'\n'
            f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
        ),
    )
    yield (
        5,
        6000,
        user,
        0,
        (
            f'Are you sure to buy the 5th relationship slot of Satori?\n'
            f'\n'
            f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_buy_relationship_slot_confirmation_description(
    new_relationship_slot_count,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``produce_buy_relationship_slot_confirmation_description`` works as intended.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_buy_relationship_slot_confirmation_description(
        new_relationship_slot_count,
        required_balance,
        target_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
