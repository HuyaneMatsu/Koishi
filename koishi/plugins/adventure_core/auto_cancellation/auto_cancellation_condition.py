__all__ = ('AutoCancellationCondition', 'auto_cancellation_condition_create')

from scarletio import RichAttributeErrorBaseType


class AutoCancellationCondition(RichAttributeErrorBaseType):
    """
    A condition of an auto cancellation rule.
    
    Attributes
    ----------
    condition : `int`
        The condition's identifier.
    
    threshold : `int`
        Threshold value.
    """
    __slots__ = ('condition', 'threshold')


def auto_cancellation_condition_create(condition, threshold):
    """
    Creates a new auto cancellation condition.
    
    Parameters
    ----------
    condition : `int`
        Condition identifier.
    
    threshold : `int`
        Threshold value.
    
    Returns
    -------
    auto_cancellation_condition : ``AutoCancellationCondition``
    """
    auto_cancellation_condition = object.__new__(AutoCancellationCondition)
    auto_cancellation_condition.condition = condition
    auto_cancellation_condition.threshold = threshold
    return auto_cancellation_condition
