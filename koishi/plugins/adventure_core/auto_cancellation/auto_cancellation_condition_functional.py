__all__ = ('AutoCancellationConditionFunctional', 'auto_cancellation_condition_functional_create')

from scarletio import RichType


class AutoCancellationConditionFunctional(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    A functional condition of an auto cancellation rule.
    
    Attributes
    ----------
    function : `(object) : bool`
        Function to execute.
    
    name : `str`
        The name of the condition.
    """
    __slots__ = ('function', 'name')


def auto_cancellation_condition_functional_create(name, function):
    """
    Creates a new auto cancellation condition functional.
    
    Parameters
    ----------
    name : `str`
        The name of the condition.
    
    function : `(object) : bool`
        Function to execute.
    
    Returns
    -------
    auto_cancellation_condition_functional : ``AutoCancellationConditionFunctional``
    """
    auto_cancellation_condition_functional = object.__new__(AutoCancellationConditionFunctional)
    auto_cancellation_condition_functional.function = function
    auto_cancellation_condition_functional.name = name
    return auto_cancellation_condition_functional
