__all__ = ('get_modifier_name_and_amount_postfix', 'construct_modifier_type')

from .modifier_kinds import (
    MODIFIER_KIND_POSTFIX_DEFAULT, MODIFIER_KIND_POSTFIXES, MODIFIER_KIND_MASK, MODIFIER_KIND_SHIFT
)
from .modifier_ids import MODIFIER_ID_NAME_DEFAULT, MODIFIER_ID_NAMES


def get_modifier_name_and_amount_postfix(modifier_type):
    """
    Gets how the modifier should be displayed.
    
    Parameters
    ----------
    modifier_type : `int`
        The modifier type to display.
    
    Returns
    -------
    modifier_name_and_amount_postfix : `(str, None | str)`
        The modifier's name and postfix to add after its value.
    """
    return (
        MODIFIER_ID_NAMES.get(modifier_type >> MODIFIER_KIND_SHIFT, MODIFIER_ID_NAME_DEFAULT),
        MODIFIER_KIND_POSTFIXES.get(modifier_type & MODIFIER_KIND_MASK, MODIFIER_KIND_POSTFIX_DEFAULT),
    )


def construct_modifier_type(modifier_id, modifier_kind):
    """
    Constructs a modifier type from the given modifier identifier and kind.
    
    Parameters
    ----------
    modifier_id : `int`
        The modifier's identifier.
    
    modifier_kind : `int`
        The modifier's kind.
    
    Returns
    -------
    modifier_type : `int`
    """
    return (modifier_id << MODIFIER_KIND_SHIFT) | modifier_kind
