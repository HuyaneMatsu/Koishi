__all__ = (
    'build_component_invoke_relationship_divorces_decrement_purchase_other',
    'build_component_invoke_relationship_divorces_decrement_purchase_self',
)

from hata import create_button

from .custom_ids import CUSTOM_ID_BURN_DIVORCE_PAPERS_BUILDER


def build_component_invoke_relationship_divorces_decrement_purchase_self():
    """
    Builds a component to invoke relationship divorces decrement for yourself.
    
    Returns
    -------
    component : ``Component``
    """
    return create_button(
        'Burn the divorce papers!',
        custom_id = CUSTOM_ID_BURN_DIVORCE_PAPERS_BUILDER(0),
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
    return create_button(
        'Burn the divorce papers!',
        custom_id = CUSTOM_ID_BURN_DIVORCE_PAPERS_BUILDER(user_id),
    )
