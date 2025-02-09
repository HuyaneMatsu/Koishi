__all__ = (
    'build_component_invoke_relationship_divorces_decrement_purchase_other',
    'build_component_invoke_relationship_divorces_decrement_purchase_self',
    'build_component_question_relationship_divorces_decrement_purchase_other',
    'build_component_question_relationship_divorces_decrement_purchase_self'
)

from hata.ext.slash import Button, Row

from .constants import (
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_BUILDER,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_BUILDER,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_BUILDER,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF,
    EMOJI_NO, EMOJI_YES
)


def build_component_invoke_relationship_divorces_decrement_purchase_self():
    """
    Builds a component to invoke relationship divorces decrement for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return Button(
        'Burn the divorce papers!',
        custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF,
    )


def build_component_invoke_relationship_divorces_decrement_purchase_other(user_id):
    """
    Builds a component to invoke relationship divorces decrement for someone else.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return Button(
        'Burn the divorce papers!',
        custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_BUILDER(user_id),
    )


def build_component_question_relationship_divorces_decrement_purchase_self():
    """
    Builds a (row) component to invoke relationship divorces decrement for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return Row(
        Button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF,
        ),
        Button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF,
        ),
    )


def build_component_question_relationship_divorces_decrement_purchase_other(user_id):
    """
    Builds a (row) component to invoke relationship divorces decrement for someone else.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return Row(
        Button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_BUILDER(user_id),
        ),
        Button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_BUILDER(user_id),
        ),
    )
