__all__ = ('Return', 'return_create')

from scarletio import RichType


class Return(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents a return.
    
    Attributes
    ----------
    id : `int`
        The identifier of the return.
    
    name : `str`
        The return's name.
    """
    __slots__ = ('id', 'name')


def return_create(return_id, name):
    """
    Creates a new return.
    
    Parameters
    ----------
    return_id : `int`
        The identifier of the return.
    
    name : `str`
        The return's name.
    
    Returns
    -------
    return_ : ``Return``
    """
    return_ = object.__new__(Return)
    return_.id = return_id
    return_.name = name
    return return_
