__all__ = (
    'build_component_invoke_relationship_slot_purchase_other', 'build_component_invoke_relationship_slot_purchase_self',
)

from hata import create_button

from .custom_ids import CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_BUILDER


def build_component_invoke_relationship_slot_purchase_self():
    """
    Builds a component to invoke relationship purchase for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return create_button(
        'I want some More! More!',
        custom_id = CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_BUILDER(0),
    )


def build_component_invoke_relationship_slot_purchase_other(user_id):
    """
    Builds a component to invoke relationship purchase for someone else.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return create_button(
        'Buy one relationship slot for them <3',
        custom_id = CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_BUILDER(user_id),
    )
