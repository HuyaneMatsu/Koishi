import vampytest
from hata import InteractionEvent, InteractionType, Message, MessageInteraction

from ..commands import is_interaction_chained


def _iter_options():
    yield (
        InteractionEvent.precreate(
            202409120001,
        ),
        False,
    )
    
    yield (
        InteractionEvent.precreate(
            202409120002,
            message = Message.precreate(
                202409120003,
            ),
        ),
        True,
    )
    
    yield (
        InteractionEvent.precreate(
            202409120004,
            message = Message.precreate(
                202409120005,
                interaction = MessageInteraction.precreate(
                    202409120006,
                    interaction_type = InteractionType.message_component,
                )
            ),
        ),
        True,
    )
    
    yield (
        InteractionEvent.precreate(
            202409120007,
            message = Message.precreate(
                202409120008,
                interaction = MessageInteraction.precreate(
                    202409120009,
                    interaction_type = InteractionType.application_command,
                )
            ),
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_interaction_chained(interaction_event):
    """
    Tests whether ``is_interaction_chained`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `bool`
    """
    output = is_interaction_chained(interaction_event)
    vampytest.assert_instance(output, bool)
    return output
