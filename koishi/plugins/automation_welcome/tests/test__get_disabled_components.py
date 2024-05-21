import vampytest
from hata import Component, ComponentType, InteractionEvent, Message

from ..interactions import get_disabled_components


def _iter_options():
    yield (
        InteractionEvent(),
        None,
    )
    
    yield (
        InteractionEvent(
            message = Message(),
        ),
        None,
    )
    
    yield (
        InteractionEvent(
            message = Message(
                components = [
                    Component(
                        ComponentType.row,
                        components = [
                            Component(
                                ComponentType.button,
                                custom_id = 'miau',
                            ),
                            Component(
                                ComponentType.button,
                                custom_id = 'meow',
                            ),
                        ],
                    ),
                ],
            ),
        ),
        [
            Component(
                ComponentType.row,
                components = [
                    Component(
                        ComponentType.button,
                        custom_id = 'miau',
                        enabled = False,
                    ),
                    Component(
                        ComponentType.button,
                        custom_id = 'meow',
                        enabled = False,
                    ),
                ],
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_disabled_components(event):
    """
    Tests whether ``get_disabled_components`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Interaction event to test with.
    
    Returns
    -------
    output : `None | list<Component>`
    """
    output = get_disabled_components(event)
    vampytest.assert_instance(output, list, nullable = True)
    return output
