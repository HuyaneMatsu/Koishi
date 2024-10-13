__all__ = ('EntryProxySaver',)

from itertools import count

from hata import KOKORO
from scarletio import RichAttributeErrorBaseType, Task, copy_docs

from ..models import DB_ENGINE


COUNTER = iter(count(1))


class EntryProxySaver(RichAttributeErrorBaseType):
    """
    Used to save entry proxies.
    
    Attributes
    ----------
    entry_proxy : ``EntryProxy``
        Entry proxy to save.
    
    ensured_for_deletion : `bool`
        Whether the entry should be deleted.
    
    modified_fields : `None | dict<str, object>`
        The fields to modify.
    
    run_task : `None | Task<.run>`
        Whether the saver is already running.
    """
    __slots__ = ('entry_proxy', 'ensured_for_deletion', 'modified_fields', 'run_task')
    
    def __new__(cls, entry_proxy):
        """
        Creates a new entry proxy saver.
        
        Parameters
        ----------
        entry_proxy : ``EntryProxy``
            The entry proxy to save.
        """
        self = object.__new__(cls)
        self.entry_proxy = entry_proxy
        self.ensured_for_deletion = False
        self.modified_fields = None
        self.run_task = None
        return self
    
    
    def __repr__(self):
        """Returns the representation of the entry proxy saver."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' entry_proxy = ')
        repr_parts.append(repr(self.entry_proxy))
        
        running = self.running
        if running:
            repr_parts.append(', running = ')
            repr_parts.append(repr(running))
        
        ensured_for_deletion = self.ensured_for_deletion
        if ensured_for_deletion:
            repr_parts.append(', ensured_for_deletion = ')
            repr_parts.append(repr(ensured_for_deletion))
        
        modified_fields = self.modified_fields
        if (modified_fields is not None):
            repr_parts.append(', modified_fields = ')
            repr_parts.append(repr(modified_fields))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def add_modification(self, field_name, field_value):
        """
        Adds a new modification.
        
        Parameters
        ----------
        field_name : `str`
            The modified field.
        
        field_value : `object`
            The field's new value.
        """
        modified_fields = self.modified_fields
        if (modified_fields is None):
            modified_fields = {}
            self.modified_fields = modified_fields
        
        modified_fields[field_name] = field_value
    
    
    def ensure_deletion(self):
        """
        Ensures to delete the entry.
        """
        self.ensured_for_deletion = True
    
    
    def is_modified(self):
        """
        Returns whether the saver was modified.
        """
        return self.ensured_for_deletion or (self.modified_fields is not None)
    
    
    def begin(self):
        """
        Begins saving.
        
        Returns
        -------
        save_task : `Task<.run>`
        """
        run_task = self.run_task
        if (run_task is None):
            run_task = Task(KOKORO, self.run())
            self.run_task = run_task
        
        return run_task
    
    
    async def run(self):
        """
        Runs the entry proxy saver.
        
        This method is a coroutine.
        """
        entry_proxy = self.entry_proxy
        try:
            async with DB_ENGINE.connect() as connector:
                entry_id = entry_proxy.entry_id
                # Entry new that is all
                if (entry_id == -1) and entry_proxy:
                    self.modified_fields = None
                    entry_id = await self._insert_entry(connector, entry_proxy)
                    entry_proxy.entry_id = entry_id
                
                while self.is_modified():
                    if self.ensured_for_deletion:
                        if entry_id != -1:
                            await self._delete_entry(connector, entry_id)
                            entry_proxy.entry_id = -1
                        
                        # We done!
                        return
                    
                    modified_fields = self.modified_fields
                    if (modified_fields is not None):
                        self.modified_fields = None
                        
                        if entry_id == -1:
                            entry_id = await self._insert_entry(connector, entry_proxy)
                            entry_proxy.entry_id = entry_id
                        
                        else:
                            await self._update_entry(connector, entry_id, modified_fields)
                        continue
                    
                    # No more cases
                    continue
        finally:
            self.run_task = None
            entry_proxy.saver = None
    
    
    async def _delete_entry(self, connector, entry_id):
        """
        Deletes the entry for the given identifier.
        
        This function is a coroutine.
        
        Parameters
        ----------
        connector : ``AsyncConnection``
            Database connector.
        
        entry_id ` int`
            The entry's identifier to delete.
        """
        return None
    
    
    async def _insert_entry(self, connector, entry_proxy):
        """
        Deletes the entry for the given identifier.
        
        This function is a coroutine.
        
        Parameters
        ----------
        connector : ``AsyncConnection``
            Database connector.
        
        entry_proxy : ``EntryProxy``
            The entry to insert.
        
        Returns
        -------
        entry_id : `int`
        """
        return -1
    
    
    async def _update_entry(self, connector, entry_id, modified_fields):
        """
        Updates the entry for the given identifier.
        
        This function is a coroutine.
        
        Parameters
        ----------
        connector : ``AsyncConnection``
            Database connector.
        
        entry_id ` int`
            The entry's identifier to update.
        
        modified_fields : `dict<str, object>`
            Modified fields to update.
        """
        return None
    
    
    @property
    def running(self):
        """
        Returns whether the saving is already running or nah.
        
        Returns
        -------
        running : `bool`
        """
        return (self.run_task is not None)
    
    
    # Do nothing if we do not have DB
    if DB_ENGINE is None:
        @copy_docs(run)
        async def run(self):
            entry_proxy = self.entry_proxy
            if entry_proxy.entry_id == -1:
                entry_proxy.entry_id = next(COUNTER)
                
            self.run_task = None
            entry_proxy.saver = None
