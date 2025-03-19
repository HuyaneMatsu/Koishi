__all__ = ()

from datetime import timezone as TimeZone

from hata import DATETIME_FORMAT_CODE
from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from .constants import TO_DOS
from .to_do_saver import ToDoSaver


class ToDo(EntryProxy):
    """
    Represents a cached to do.
    
    Attributes
    ----------
    created_at : `DateTime`
        When the entry was created.
    
    creator_id : `int`
        Wo created the entry.
    
    description : `str`
        The entry's description.
    
    entry_id : `int`
        The identifier of the entry in the database.
    
    name : `str`
        The entry's name.
    
    saver : `None | ToDoSaver`
        Saver responsible for save synchronization.
    """
    __slots__ = ('created_at', 'creator_id', 'description', 'name',)
    
    saver_type = ToDoSaver
    
    def __new__(cls, name, description, created_at, creator_id):
        """
        Creates a new to-do to given fields.
        
        Attributes
        ----------
        name : `str`
            The entry's name.
        
        description : `str`
            The entry's description.
        
        created_at : `DateTime`
            When the entry was created.
        
        creator_id : `int`
            Wo created the entry.
        """
        self = object.__new__(cls)
        
        self.created_at = created_at
        self.creator_id = creator_id
        self.description = description
        self.entry_id = -1
        self.name = name
        self.saver = None
        
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
            repr_parts.append(',')
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # created_at
        repr_parts.append(', created_at = ')
        repr_parts.append(format(self.created_at, DATETIME_FORMAT_CODE))
        
        # creator_id
        repr_parts.append(', creator_id = ')
        repr_parts.append(repr(self.creator_id))
    
    
    async def save(self):
        """
        Saves the entry and then caches it.
        
        This function is a coroutine.
        """
        saver = self.get_saver()
        await saver.begin()
        self._store_in_cache()
    
    
    @copy_docs(EntryProxy._store_in_cache)
    def _store_in_cache(self):
        TO_DOS[self.entry_id] = self
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del TO_DOS[self.entry_id]
        except KeyError:
            pass
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        """
        Creates an to-do from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        entry_id = entry['id']
        
        try:
            self = TO_DOS[entry_id]
        except KeyError:
            self = object.__new__(cls)
            self.entry_id = entry_id
            self.saver = None
            TO_DOS[entry_id] = self
        
        self.created_at = entry['created_at'].replace(tzinfo = TimeZone.utc)
        self.creator_id = entry['creator_id']
        self.description = entry['description']
        self.name = entry['name']
        
        return self
