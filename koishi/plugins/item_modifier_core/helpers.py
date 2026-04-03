__all__ = ('get_modifier_name_and_value_producer_and_amount_postfix', 'construct_modifier_type')

from ..unit_core import produce_kilogram, produce_meter_per_second

from .modifier_kinds import (
    MODIFIER_KIND_POSTFIX_DEFAULT, MODIFIER_KIND_POSTFIXES, MODIFIER_KIND_MASK, MODIFIER_KIND_SHIFT
)
from .modifier_ids import MODIFIER_ID__INVENTORY, MODIFIER_ID__MOVEMENT, MODIFIER_ID_NAME_DEFAULT, MODIFIER_ID_NAMES


MODIFIER_VALUE_PRODUCERS = {
    MODIFIER_ID__MOVEMENT : produce_meter_per_second,
    MODIFIER_ID__INVENTORY : produce_kilogram,
}


def get_modifier_name_and_value_producer_and_amount_postfix(modifier_type):
    """
    Gets how the modifier should be displayed.
    
    Parameters
    ----------
    modifier_type : `int`
        The modifier type to display.
    
    Returns
    -------
    modifier_name_and_value_producer_and_amount_postfix : `(str, None | GeneratorFunctionType, None | str)`
        The modifier's name and value producer and postfix to add after its value.
    """
    modifier_id = modifier_type >> MODIFIER_KIND_SHIFT
    modifier_kind = modifier_type & MODIFIER_KIND_MASK
    
    postfix = MODIFIER_KIND_POSTFIXES.get(modifier_kind, MODIFIER_KIND_POSTFIX_DEFAULT)
    
    # Do not return value producer if we have a postfix, else we will end up with things like `0.070 kg%` instead of
    # `70%`
    if postfix is None:
        value_producer = MODIFIER_VALUE_PRODUCERS.get(modifier_id, None)
    else:
        value_producer = None
    
    return (
        MODIFIER_ID_NAMES.get(modifier_id, MODIFIER_ID_NAME_DEFAULT),
        value_producer,
        postfix,
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
