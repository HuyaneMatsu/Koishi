__all__ = ()

import vampytest
from hata import Guild, InteractionEvent, Message

from ..deck import Deck
from ..session import Game21Session


def _assert_fields_set(session):
    """
    Asserts whether every field of the session are set.
    
    Parameters
    ----------
    session : ``Game21Session``
        The session to check.
    """
    vampytest.assert_instance(session, Game21Session)
    vampytest.assert_instance(session.amount, int)
    vampytest.assert_instance(session.deck, Deck)
    vampytest.assert_instance(session.guild, Guild, nullable = True)
    vampytest.assert_instance(session.id, int)
    vampytest.assert_instance(session.latest_interaction_event, InteractionEvent)
    vampytest.assert_instance(session.message, Message, nullable = True)
    vampytest.assert_instance(session.user_ids, tuple, nullable = True)


def test__Session__new():
    """
    Tests whether ``Session.__new__`` works as intended.
    """
    session_id = 556666
    guild = Guild.precreate(202408030000)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202408030001)
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    _assert_fields_set(session)
    
    vampytest.assert_eq(session.amount, amount)
    vampytest.assert_is(session.guild, guild)
    vampytest.assert_is(session.latest_interaction_event, latest_interaction_event)


def test__Session__repr():
    """
    Tests whether ``Session.__repr__`` works as intended.
    """
    session_id = 556666
    guild = Guild.precreate(202408030001)
    amount = 2000
    latest_interaction_event = InteractionEvent.precreate(202408030003)
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    
    output = repr(session)
    vampytest.assert_instance(output, str)
