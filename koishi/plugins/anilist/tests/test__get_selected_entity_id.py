import vampytest
from hata import InteractionEvent, InteractionMetadataMessageComponent, InteractionType

from ..helpers import get_selected_entity_id


def _iter_options():
    yield (
        InteractionEvent(
            interaction = InteractionMetadataMessageComponent(
                values = None,
            ),
            interaction_type = InteractionType.message_component,
        ),
        -1,
    )
    yield (
        InteractionEvent(
            interaction = InteractionMetadataMessageComponent(
                values = ['pepe'],
            ),
            interaction_type = InteractionType.message_component,
        ),
        -1,
    )
    yield (
        InteractionEvent(
            interaction = InteractionMetadataMessageComponent(
                values = ['12'],
            ),
            interaction_type = InteractionType.message_component,
        ),
        12,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_selected_entity_id(event):
    """
    Asserts whether ``get_selected_entity_id`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Interaction event to get the selected entity is from.
    
    Returns
    -------
    entity_id : `int`
    """
    return get_selected_entity_id(event)
