__all__ = ('ImageHandlerRequestBase',)

from collections import deque as Deque

from hata import KOKORO, InteractionType
from scarletio import copy_docs, Future, Task, TaskGroup

from .base import ImageHandlerBase



class ImageHandlerRequestBase(ImageHandlerBase):
    """
    Base class for request based image handlers.
    
    Attributes
    ----------
    _cache : `list` of ``ImageDetailBase``
        Additional requested card details.
    _waiters : `Deque` of ``Future``
        Waiter futures for card detail.
    _request_task : `None`, ``Task`` of ``._request_loop``
        Active request loop.
    """
    __slots__ = ('_cache', '_waiters', '_request_task')
    
    @copy_docs(ImageHandlerBase.__new__)
    def __new__(cls):
        self = object.__new__(cls)
        self._cache = []
        self._waiters = Deque()
        self._request_task = None
        return self
    
    
    @copy_docs(ImageHandlerBase.get_image)
    async def get_image(self, client, event, **acknowledge_parameters):
        cache = self._cache
        if cache:
            return cache.pop()
        
        waiter = Future(KOKORO)
        self._waiters.appendleft(waiter)
        
        self._maybe_start_request_loop(client)
        
        if (event is None):
            coroutine = None
        
        elif acknowledge_parameters:
            coroutine = client.interaction_response_message_create(
                event, **acknowledge_parameters
            )
        
        else:
            if event.type is InteractionType.application_command:
                coroutine = client.interaction_application_command_acknowledge(event)
            
            elif event.type is InteractionType.message_component:
                coroutine = client.interaction_component_acknowledge(event)
            
            else:
                coroutine = None
        
        if coroutine is None:
            return await waiter
        
        acknowledge_task = Task(KOKORO, coroutine)
        
        await TaskGroup(KOKORO, [acknowledge_task, waiter]).wait_all()
        
        try:
            acknowledge_task.get_result()
        except:
            waiter.cancel()
            raise
        
        return waiter.get_result()

    
    def _maybe_start_request_loop(self, client):
        """
        Starts ``._request_loop`` if not yet running.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        """
        if (self._request_task is None):
            self._request_task = Task(KOKORO, self._request_loop(client))
    
    
    async def _request_loop(self, client):
        """
        Keeps requesting new image details while required.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        """
        try:
            while self._waiters:
                data = await self._request(client)
                if data is None:
                    self._abort_waiters()
                    break
                
                details = self._process_data(data)
                if (details is None) or (not details):
                    self._abort_waiters()
                    break
                
                self._feed_details(details)
                continue
        
        finally:
            self._request_task = None
    
    
    async def _request(self, client):
        """
        Requests a chunk of image data.
        
        This method is a coroutine
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        
        Returns
        -------
        data : `None`, `object`
        """
        return None
    
    
    def _process_data(self, data):
        """
        Processes a chunk of data returned by ``._request``.
        
        Parameters
        ----------
        data : `object`
        
        Returns
        -------
        card_details : `None`,  list` of ``ImageDetailBase``
        """
        return None
    
    
    def _abort_waiters(self):
        """
        Aborts all waiters setting `None` as result to all future.
        """
        waiters = self._waiters
        while waiters:
            waiter = waiters.pop()
            waiter.set_result_if_pending(None)
    
    
    def _feed_details(self, details):
        """
        Feeds details to the waiters of the handler.
        
        If there are no more waiters, will extend the cache with them.
        
        Parameters
        ----------
        details : `list` of ``ImageDetailBase``
        """
        waiters = self._waiters
        while True:
            if not details:
                break
            
            if not waiters:
                # extend cache with the leftover details.
                self._cache.extend(details)
                break
            
            waiter = waiters.pop()
            if waiter.is_pending():
                waiter.set_result(details.pop())
