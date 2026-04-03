import vampytest
from hata import Guild, InteractionEvent

from ..helpers import add_user_id_to_session
from ..session import Game21Session


def test__add_user_id_to_session__no_user_ids():
    """
    Tests whether ``add_user_id_to_session`` works as intended.
    
    Case: No user id-s registered yet.
    """
    session_id = 523333
    guild = Guild.precreate(202511180000)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180001)
    
    user_id_0 = 202511180002
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    
    sessions_mock = {}
    
    mocked = vampytest.mock_globals(
        add_user_id_to_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_0)
    
    vampytest.assert_eq(session.user_ids, (user_id_0,))
    vampytest.assert_eq(sessions_mock, {session_id: session})


def test__add_user_id_to_session__with_user_ids():
    """
    Tests whether ``add_user_id_to_session`` works as intended.
    
    Case: There are user id-s already registered.
    """
    session_id = 523333
    guild = Guild.precreate(202511180010)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180011)
    
    user_id_0 = 202511180012
    user_id_1 = 202511180013
    user_id_2 = 202511180014
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    
    sessions_mock = {}
    
    mocked = vampytest.mock_globals(
        add_user_id_to_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_2)
    
    vampytest.assert_eq(session.user_ids, (user_id_0, user_id_1, user_id_2))
    vampytest.assert_eq(sessions_mock, {})


def test__add_user_id_to_session__with_present_user_id():
    """
    Tests whether ``add_user_id_to_session`` works as intended.
    
    Case: User id already present.
    """
    session_id = 523333
    guild = Guild.precreate(202511180020)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202511180021)
    
    user_id_0 = 202511180022
    user_id_1 = 202511180023
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    
    sessions_mock = {}
    
    mocked = vampytest.mock_globals(
        add_user_id_to_session,
        SESSIONS = sessions_mock,
    )
    
    mocked(session, user_id_1)
    
    vampytest.assert_eq(session.user_ids, (user_id_0, user_id_1))
    vampytest.assert_eq(sessions_mock, {})
