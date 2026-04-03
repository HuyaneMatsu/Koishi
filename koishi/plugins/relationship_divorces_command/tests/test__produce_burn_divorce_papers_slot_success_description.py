import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_burn_divorce_papers_success_description


def _iter_options():
    user = User.precreate(
        202511300010,
        name = 'Satori',
    )
    
    yield (
        5,
        7000,
        6000,
        None,
        0,
        (
            f'The hired ninjas successfully located and burnt your 5th divorce papers.\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'7000 \x1b[31m->\x1b[0m 1000\n'
            f'```'
        ),
    )
    yield (
        5,
        7000,
        6000,
        user,
        0,
        (
            f'The hired ninjas successfully located and burnt Satori\'s 5th divorce papers.\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'7000 \x1b[31m->\x1b[0m 1000\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_burn_divorce_papers_success_description(
    relationship_divorces,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``produce_burn_divorce_papers_success_description`` works as intended.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
    current_balance : `int`
        The user's current balance.
    
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
    output = [*produce_burn_divorce_papers_success_description(
        relationship_divorces,
        current_balance,
        required_balance,
        target_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
