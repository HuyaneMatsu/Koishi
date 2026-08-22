__all__ = ('getter_setter_pair_create',)


def getter_setter_pair_create():
    """
    Creates an returns a getter & setter pair.
    
    Returns
    --------
    getter_setter_pair : `(FunctionType, FunctionType)`
    """
    value = None
        
    def getter():
        """
        Gets the value.
        
        Returns
        -------
        value : `None | object`
        """
        nonlocal value
        return value
    
    def setter(input_value):
        """
        Sets the value.
        
        Parameters
        ----------
        input_value : `óNone | object`
            Value to set.
        """
        nonlocal value
        value = input_value
    
    return getter, setter
