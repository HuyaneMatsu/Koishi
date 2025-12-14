import vampytest

from hata import Component, create_button

from ..component_builders import build_component_invoke_relationship_slot_purchase_other


def _iter_options():
    user_id = 202501260000
    
    yield (
        user_id,
        create_button(
            'Buy one relationship slot for them <3',
            custom_id = f'user.buy_relationship_slots.invoke.{user_id:x}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_invoke_relationship_slot_purchase_other(user_id):
    """
    tests whether ``build_component_invoke_relationship_slot_purchase_other`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_invoke_relationship_slot_purchase_other(user_id)
    vampytest.assert_instance(output, Component)
    return output
