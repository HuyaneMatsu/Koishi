import vampytest

from hata import Component, create_button

from ..component_builders import build_component_invoke_relationship_slot_purchase_self


def _iter_options():
    yield (
        create_button(
            'I want some More! More!',
            custom_id = 'user_balance.relationship_slots.increment.invoke.self'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_invoke_relationship_slot_purchase_self():
    """
    tests whether ``build_component_invoke_relationship_slot_purchase_self`` works as intended.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_invoke_relationship_slot_purchase_self()
    vampytest.assert_instance(output, Component)
    return output
