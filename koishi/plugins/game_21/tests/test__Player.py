__all__ = ()

import vampytest
from hata import ClientUserBase, InteractionEvent, User

from ..hand import Hand
from ..player import Player


def _assert_fields_set(player):
    """
    Asserts whether every field of the player are set.
    
    Parameters
    ----------
    player : ``Player``
        The player to check.
    """
    vampytest.assert_instance(player, Player)
    vampytest.assert_instance(player.hand, Hand)
    vampytest.assert_instance(player.entry_id, int)
    vampytest.assert_instance(player.latest_interaction_event, InteractionEvent)
    vampytest.assert_instance(player.result, int)
    vampytest.assert_instance(player.user, ClientUserBase)


def test__Player__new():
    """
    Tests whether ``Player.__new__`` works as intended.
    """
    entry_id = 2000
    latest_interaction_event = InteractionEvent.precreate(202408030004)
    user = User.precreate(202408030005)
    
    player = Player(user, entry_id, latest_interaction_event)
    
    vampytest.assert_eq(player.entry_id, entry_id)
    vampytest.assert_is(player.latest_interaction_event, latest_interaction_event)
    vampytest.assert_is(player.user, user)


def test__Player__repr():
    """
    Tests whether ``Player.__repr__`` works as intended.
    """
    entry_id = 2000
    latest_interaction_event = InteractionEvent.precreate(202408030006)
    user = User.precreate(202408030007)
    
    player = Player(user, entry_id, latest_interaction_event)
    
    output = repr(player)
    vampytest.assert_instance(output, str)
