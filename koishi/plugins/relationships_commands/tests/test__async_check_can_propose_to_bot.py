import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ..checks import async_check_can_propose_to_bot


def _iter_options__passing():
    user_id_0 = 202501100000
    user_id_1 = 202501100001
    user_id_2 = 202502240020
    
    user_0 = User.precreate(user_id_0, name = 'Satori', bot = True)
    user_1 = User.precreate(user_id_1, name = 'Koishi', bot = False)
    user_2 = User.precreate(user_id_2)
    
    yield (
        user_2,
        user_0,
        0,
        1,
        0,
    )
    
    yield (
        user_2,
        user_1,
        2,
        1,
        0,
    )


def _iter_options__failing():
    user_id_0 = 202501100002
    user_id_1 = 202502240021
    
    user_0 = User.precreate(user_id_0, name = 'Satori', bot = True)
    user_1 = User.precreate(user_id_1)
    
    yield (
        user_1,
        user_0,
        1,
        1,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
async def test__async_check_can_propose_to_bot(
    source_user, target_user, target_relationship_count, target_relationship_slots, guild_id
):
    """
    Tests whether ``async_check_can_propose_to_bot`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    target_relationship_count : `int`
        The amount of relationships the target user have.
    
    target_relationship_slots : `int`
        The amount of relationships the target user can have.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mocked_can_gift_with_request(passed_source_user, passed_target_user):
        nonlocal source_user
        nonlocal target_user
        
        vampytest.assert_is(source_user, passed_source_user)
        vampytest.assert_is(target_user, passed_target_user)
        
        return True
    
    mocked = vampytest.mock_globals(
        async_check_can_propose_to_bot,
        can_gift_with_request = mocked_can_gift_with_request,
    )
    
    await mocked(
        source_user, target_user, target_relationship_count, target_relationship_slots, guild_id
    )
