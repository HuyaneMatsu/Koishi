import vampytest

from hata import InteractionEvent, User

from ..helpers import store_event
from ..player import Player
from ..session import Session


def _iter_options():
    interaction_event_0 = InteractionEvent.precreate(202408040002)
    interaction_event_1 = InteractionEvent.precreate(202408040003)
    interaction_event_2 = InteractionEvent.precreate(202408040004)
    player = Player(User.precreate(202408040005), -1, interaction_event_0)
    session = Session(None, 1000, interaction_event_1)
    
    yield (
        player,
        session,
        True,
        interaction_event_2,
        (interaction_event_2, interaction_event_2),
    )


    interaction_event_0 = InteractionEvent.precreate(202408040006)
    interaction_event_1 = InteractionEvent.precreate(202408040007)
    interaction_event_2 = InteractionEvent.precreate(202408040008)
    player = Player(User.precreate(202408040009), -1, interaction_event_0)
    session = Session(None, 1000, interaction_event_1)
    
    yield (
        player,
        session,
        False,
        interaction_event_2,
        (interaction_event_2, interaction_event_1),
    )


    interaction_event_0 = InteractionEvent.precreate(202408040010)
    interaction_event_1 = InteractionEvent.precreate(202408040011)
    interaction_event_2 = InteractionEvent.precreate(202408040012)
    player = Player(User.precreate(202408040013), -1, interaction_event_1)
    session = Session(None, 1000, interaction_event_2)
    
    yield (
        player,
        session,
        True,
        interaction_event_0,
        (interaction_event_1, interaction_event_2),
    )


    interaction_event_0 = InteractionEvent.precreate(202408040062)
    interaction_event_1 = InteractionEvent.precreate(202408040063)
    player = None
    session = Session(None, 1000, interaction_event_1)
    
    yield (
        player,
        session,
        True,
        interaction_event_0,
        (None, interaction_event_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__store_event(player, session, single_player, interaction_event):
    """
    Tests whether ``store_event`` works as intended.
    
    Parameters
    ----------
    player : `None | Player`
        The respective player.
    session : ``Session``
        The respective session.
    single_player : `bool`
        Whether the game mode is single player.
    interaction_event : ``InteractionEvent``
        The interaction event to store.
    
    Returns
    -------
    output : `(None | InteractionEvent, InteractionEvent)`
    """
    store_event(player, session, single_player, interaction_event)
    return (
        None if player is None else player.latest_interaction_event,
        session.latest_interaction_event,
    )
