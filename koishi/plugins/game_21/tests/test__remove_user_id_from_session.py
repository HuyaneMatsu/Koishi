import vampytest
from hata import Guild, InteractionEvent

from ..helpers import remove_user_id_from_session
from ..session import Game21Session


def test__remove_user_id_from_session__no_user_ids():
    """
    Tests whether ``remove_user_id_from_session`` works as intended.
    
    Case: No user id-s registered yet.
    """
    session_id = 523333
    guild = Guild.precreate(202511180040)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180041)
    
    user_id_0 = 202511180042
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    
    sessions_mock = {}
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_0)
    
    vampytest.assert_eq(session.user_ids, None)
    vampytest.assert_eq(sessions_mock, {})


def test__remove_user_id_from_session__with_user_ids():
    """
    Tests whether ``remove_user_id_from_session`` works as intended.
    
    Case: There are user id-s already registered.
    """
    session_id = 523333
    guild = Guild.precreate(202511180050)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180051)
    
    user_id_0 = 202511180052
    user_id_1 = 202511180053
    user_id_2 = 202511180054
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    
    sessions_mock = {session_id: session}
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_2)
    
    vampytest.assert_eq(session.user_ids, (user_id_0, user_id_1))
    vampytest.assert_eq(sessions_mock, {session_id: session})


def test__remove_user_id_from_session__with_present_user_id():
    """
    Tests whether ``remove_user_id_from_session`` works as intended.
    
    Case: User id already present.
    """
    session_id = 523333
    guild = Guild.precreate(202511180060)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180061)
    
    user_id_0 = 202511180062
    user_id_1 = 202511180063
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    
    sessions_mock = {session_id: session}
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_1)
    
    vampytest.assert_eq(session.user_ids, (user_id_0,))
    vampytest.assert_eq(sessions_mock, {session_id: session})


def test__remove_user_id_from_session__removing_last_user_id():
    """
    Tests whether ``remove_user_id_from_session`` works as intended.
    
    Case: Removing last user id.
    """
    session_id = 523333
    guild = Guild.precreate(202511180070)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180071)
    
    user_id_0 = 202511180072
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0,)
    
    sessions_mock = {session_id: session}
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_0)
    
    vampytest.assert_eq(session.user_ids, None)
    vampytest.assert_eq(sessions_mock, {})
