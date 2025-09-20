import vampytest
from hata import ComponentType, InteractionComponent, InteractionEvent, InteractionType

from ..helpers import get_selected_entity_id


def _iter_options():
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            component = InteractionComponent(
                ComponentType.string_select,
                custom_id = 'select',
            ),
        ),
        -1,
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            component = InteractionComponent(
                ComponentType.string_select,
                custom_id = 'select',
                values = ['pepe'],
            ),
        ),
        -1,
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            component = InteractionComponent(
                ComponentType.string_select,
                custom_id = 'select',
                values = ['12'],
            ),
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
    output = get_selected_entity_id(event)
    vampytest.assert_instance(output, int)
    return output
