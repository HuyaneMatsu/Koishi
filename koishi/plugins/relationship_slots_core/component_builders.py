__all__ = (
    'build_component_invoke_relationship_slot_purchase_other', 'build_component_invoke_relationship_slot_purchase_self',
    'build_component_question_relationship_slot_purchase_other', 'build_component_question_relationship_slot_purchase_self'
)

from hata import create_button, create_row

from .constants import (
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_OTHER_BUILDER, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_SELF,
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_OTHER_BUILDER, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_SELF,
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_OTHER_BUILDER, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_SELF,
    EMOJI_NO, EMOJI_YES
)


def build_component_invoke_relationship_slot_purchase_self():
    """
    Builds a component to invoke relationship purchase for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return create_button(
        'I want some More! More!',
        custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_SELF,
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
        custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_OTHER_BUILDER(user_id),
    )


def build_component_question_relationship_slot_purchase_self():
    """
    Builds a (row) component to confirm relationship purchase for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return create_row(
        create_button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_SELF,
        ),
        create_button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_SELF,
        ),
    )


def build_component_question_relationship_slot_purchase_other(user_id):
    """
    Builds a (row) component to confirm relationship purchase for someone else.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return create_row(
        create_button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_OTHER_BUILDER(user_id),
        ),
        create_button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_OTHER_BUILDER(user_id),
        ),
    )
