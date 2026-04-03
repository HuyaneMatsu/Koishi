import vampytest
from hata import Guild, InteractionEvent

from ..helpers import remove_user_ids_from_session
from ..session import Game21Session


def test__remove_user_ids_from_session__no_user_ids():
    """
    Tests whether ``remove_user_ids_from_session`` works as intended.
    
    Case: No user id-s registered yet.
    """
    session_id = 523333
    guild = Guild.precreate(202511180080)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180081)
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    
    sessions_mock = {}
    
    mocked = vampytest.mock_globals(
        remove_user_ids_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session)
    
    vampytest.assert_eq(session.user_ids, None)
    vampytest.assert_eq(sessions_mock, {})


def test__remove_user_ids_from_session__with_user_ids():
    """
    Tests whether ``remove_user_ids_from_session`` works as intended.
    
    Case: There are user id-s already registered.
    """
    session_id = 523333
    guild = Guild.precreate(202511180090)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180091)
    
    user_id_0 = 202511180092
    user_id_1 = 202511180093
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    
    sessions_mock = {session_id: session}
    
    mocked = vampytest.mock_globals(
        remove_user_ids_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session)
    
    vampytest.assert_eq(session.user_ids, None)
    vampytest.assert_eq(sessions_mock, {})
