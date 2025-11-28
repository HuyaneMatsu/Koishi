__all__ = ()

from scarletio import RichAttributeErrorBaseType


class UserBalanceAllocationHook(RichAttributeErrorBaseType):
    """
    Hook into user balance.
    
    Attributes
    ----------
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    get_session_enty : `None | CoroutineFunction`
        A function to get the session's entry.
    
    is_allocation_alive_sync : `None | FunctionType`
        Sync check whether the allocation is alive.
    """
    __slots__ = ('allocation_feature_id', 'get_session_enty', 'is_allocation_alive_sync')
    
    def __new__(cls, allocation_feature_id, is_allocation_alive_sync, get_session_enty):
        """
        Creates a new user balance allocation hook.
        
        Parameters
        ----------
        allocation_feature_id : `int`
            The allocation feature's identifier.
        
        is_allocation_alive_sync : `None | FunctionType`
            Sync check whether the allocation is alive.
        
        get_session_enty : `None | CoroutineFunction`
            A function to get the session's entry.
        """
        self = object.__new__(cls)
        self.allocation_feature_id = allocation_feature_id
        self.get_session_enty = get_session_enty
        self.is_allocation_alive_sync = is_allocation_alive_sync
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' allocation_feature_id = ')
        repr_parts.append(repr(self.allocation_feature_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
