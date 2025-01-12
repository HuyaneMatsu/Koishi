import vampytest
from hata import InteractionEvent, InteractionMetadataMessageComponent, InteractionType, User, Message, MessageInteraction

from ..helpers import is_event_user_same


def _iter_options():
    user_id = 202403310000
    user = User.precreate(user_id)
    
    yield (
        InteractionEvent(
            user = None,
            message = None,
        ),
        False,
    )
    yield (
        InteractionEvent(
            user = user,
            message = None
        ),
        False,
    )
    
    yield (
        InteractionEvent(
            user = None,
            message = Message(),
        ),
        False,
    )
    yield (
        InteractionEvent(
            user = user,
            message = Message(),
        ),
        False,
    )
    
    # Both has `ZEROUSER` as `.user`, so it actually returns `True`.
    yield (
        InteractionEvent(
            user = None,
            message = Message(interaction = MessageInteraction()),
        ),
        True,
    )
    yield (
        InteractionEvent(
            user = user,
            message = Message(interaction = MessageInteraction()),
        ),
        False,
    )

    yield (
        InteractionEvent(
            user = None,
            message = Message(interaction = MessageInteraction(user = user)),
        ),
        False,
    )
    yield (
        InteractionEvent(
            user = user,
            message = Message(interaction = MessageInteraction(user = user)),
        ),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_event_user_same(event):
    """
    Asserts whether ``is_event_user_same`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Interaction event to get whether the user is the same
    
    Returns
    -------
    is_same : `bool`
    """
    return is_event_user_same(event)
