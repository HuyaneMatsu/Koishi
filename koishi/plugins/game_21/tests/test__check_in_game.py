import vampytest

from hata import InteractionEvent, User
from hata.ext.slash import InteractionAbortedError

from ....bot_utils.constants import IN_GAME_IDS

from ..checks import check_in_game


def _iter_options():
    user_id = 202408020002
    
    yield (
        [],
        user_id,
        False,
    )

    yield (
        [user_id],
        user_id,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_in_game(in_game_user_ids, user_id):
    """
    Tests whether ``check_in_game`` works as intended.
    
    Parameters
    ----------
    in_game_user_ids : `list<int>`
        User identifiers who are in game already.
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    aborted : `bool`
    """
    event = InteractionEvent(user = User.precreate(user_id))
    
    for in_game_user_id in in_game_user_ids:
        IN_GAME_IDS.add(in_game_user_id)
    
    try:
        try:
            check_in_game(event)
        except InteractionAbortedError:
            return True
        
        return False
    
    finally:
        for in_game_user_id in in_game_user_ids:
            IN_GAME_IDS.discard(in_game_user_id)
