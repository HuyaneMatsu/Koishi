import vampytest

from hata import InteractionEvent

from ..helpers import iter_interaction_events


def _iter_options():
    interaction_event_0 = InteractionEvent.precreate(202408040000)
    interaction_event_1 = InteractionEvent.precreate(202408040001)
    
    yield (
        interaction_event_0,
        interaction_event_1,
        [interaction_event_0, interaction_event_1],
    )
    
    yield (
        interaction_event_0,
        interaction_event_0,
        [interaction_event_0],
    )

    
    yield (
        None,
        interaction_event_0,
        [interaction_event_0],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_interaction_events(interaction_event, previous_interaction_event):
    """
    Tests whether ``iter_interaction_events`` works as intended.
    
    Parameters
    ----------
    interaction_event : `None | InteractionEvent`
        Interaction event.
    previous_interaction_event : `InteractionEvent`
        The previous interaction event.
    
    Returns
    -------
    output : `list<InteractionEvent>`
    """
    output = [*iter_interaction_events(interaction_event, previous_interaction_event)]
    
    for element in output:
        vampytest.assert_instance(element, InteractionEvent)
    
    return output
