__all__ = ('EntryProxy',)

from scarletio import RichAttributeErrorBaseType

from .entry_proxy_saver import EntryProxySaver
from .entry_proxy_type import EntryProxyType


class EntryProxy(RichAttributeErrorBaseType, metaclass = EntryProxyType):
    """
    Entry proxy.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    saver : `None | EntryProxySaver`
        Saver responsible for save synchronization.
    """
    __slots__ = ('entry_id', 'saver')
    
    field_setters = {}
    saver_type = EntryProxySaver
    
    def __new__(cls):
        """
        Creates a new automation config.
        """
        self = object.__new__(cls)
        self.entry_id = 0
        self.saver = None
        return self
    
    
    def __repr__(self):
        """Returns the entry proxy's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id != 0:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            field_added = True
        
        else:
            field_added = False
        
        
        self._put_repr_parts(repr_parts, field_added)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts(self, repr_parts, field_added):
        """
        Helper function for `__repr__`` to add additional fields into it.
        
        Parameters
        ----------
        repr_parts : `list<str>`
            Representation parts to extend.
        
        field_added : `bool`
            Whether any field(s) where already added.
        """
        return
    
    
    def __bool__(self):
        """Returns whether any entry proxy is set."""
        return True
    
    
    def get_saver(self):
        """
        Gets or creates a new saver for the configuration.
        """
        saver = self.saver
        if (saver is None):
            saver = self.saver_type(self)
            self.saver = saver
        
        return saver
    
    
    def set(self, field_name, field_value):
        """
        Sets a value of the auto moderation configuration.
        
        Parameters
        ----------
        field_name : `str`
            The field's name.
        
        field_value : `object`
            The new value of the field.
        """
        self.field_setters[field_name](self, field_value)
        
        saver = self.get_saver()
        
        if self:
            self._store_in_cache()
            saver.add_modification(field_name, field_value)
        
        else:
            saver.ensure_deletion()
            self._pop_from_cache()
        
        saver.begin()
    
    
    def delete(self):
        """
        Deletes the entry.
        """
        saver = self.get_saver()
        saver.ensure_deletion()
        saver.begin()
        self._pop_from_cache()
    
    
    def _store_in_cache(self):
        """
        Stores self in cache.
        """
        return None
    
    
    def _pop_from_cache(self):
        """
        Removes self from cache.
        """
        return None
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an entry proxy from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = 0
        return self
