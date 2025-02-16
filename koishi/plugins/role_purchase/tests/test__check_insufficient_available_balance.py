import vampytest
from hata import Role
from hata.ext.slash import InteractionAbortedError

from ..checks import check_insufficient_available_balance


def _iter_options__passing():
    role_id = 202502140000
    guild_id = 202502140001
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield role, 200, 199
    yield role, 200, 200


def _iter_options__failing():
    role_id = 202502140002
    guild_id = 202502140003
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield role, 200, 201


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_insufficient_available_balance(role, available_balance, required_balance):
    """
    Tests whether ``check_insufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    available_balance : `int`
        Available balance.
    
    required_balance : `int`
        The required balance to buy the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_insufficient_available_balance(role, available_balance, required_balance)
