__all__ = ('StageResult',)

from scarletio import RichAttributeErrorBaseType


class StageResult(RichAttributeErrorBaseType):
    """
    Represents a user's state of a stage.
    
    Attributes
    ----------
    best : `int`
        The user's best solution of the stage.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    stage_id : `int`
        The stage's identifier.
    """
    __slots__ = ('best', 'entry_id', 'stage_id')
    
    
    def __new__(cls, entry_id, stage_id, best):
        """
        Creates a new stage state from the given parameters.
        
        Parameters
        ----------
        entry_id : `int`
            The entry's identifier in the database.
        
        stage_id : `int`
            The stage's identifier.
        
        best : `int`
            The user's best solution of the stage.
        """
        self = object.__new__(cls)
        self.entry_id = entry_id
        self.stage_id = stage_id
        self.best = best
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        repr_parts.append(' entry_id = ')
        repr_parts.append(repr(self.entry_id))
        
        # stage_id
        repr_parts.append(', stage_id = ')
        repr_parts.append(repr(self.stage_id))
        
        # best
        repr_parts.append(', best = ')
        repr_parts.append(repr(self.best))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # entry_id
        if self.entry_id != other.entry_id:
            return False
        
        # stage_id
        if self.stage_id != other.stage_id:
            return False
        
        # best
        if self.best != other.best:
            return False
        
        return True
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates a new stage result from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            Database entry.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.stage_id = entry['stage_id']
        self.best = entry['best']
        return self
