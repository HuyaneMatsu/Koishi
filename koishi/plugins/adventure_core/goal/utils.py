__all__ = ('produce_goal',)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import get_item
from ...unit_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_NAME_DEFAULT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT, produce_weight
)
from .goal import GOAL_TYPE_ITEM_EXACT


def produce_goal(goal):
    """
    Produces the goal's representation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    goal : ``Goal``
        Goal to produce.
    
    Yields
    ------
    part : `str`
    """
    goal_type = goal.behaviour.type
    configuration = goal.configuration
    
    if goal_type == GOAL_TYPE_ITEM_EXACT:
        amount_type = configuration.amount_type
        amount_required = configuration.amount_required
        
        if amount_type == AMOUNT_TYPE_WEIGHT:
            yield from produce_weight(amount_required)
            yield ' kg'
        
        else:
            yield str(amount_required)
            
            if amount_type == AMOUNT_TYPE_COUNT:
                pass
            
            elif amount_type == AMOUNT_TYPE_VALUE:
                yield ' '
                yield EMOJI__HEART_CURRENCY.as_emoji
                yield ' worth of'
            
            else:
                yield AMOUNT_TYPE_NAME_DEFAULT
        
        yield ' '
        item = get_item(configuration.item_id)
        emoji = item.emoji
        if (emoji is not None):
            yield emoji.as_emoji
            yield ' '
        
        yield item.name
        
    
    else:
        # No other cases
        yield '\*none\*'
