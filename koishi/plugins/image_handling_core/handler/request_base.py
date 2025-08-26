__all__ = ('ImageHandlerRequestBase',)

from collections import deque as Deque

from hata import KOKORO
from scarletio import copy_docs, Future, Task
from scarletio.http_client import HTTPClient

from .base import ImageHandlerBase


HTTP_CLIENT = HTTPClient(KOKORO)


class ImageHandlerRequestBase(ImageHandlerBase):
    """
    Base class for request based image handlers.
    
    Attributes
    ----------
    _cache : ``list<ImageDetailBase>``
        Additional requested image details.
    
    _request_task : ``None | Task<._request_loop>``
        Active request loop.
    
    _waiters : ``Deque<Future>``
        Waiter futures for image detail.
    """
    __slots__ = ('_cache', '_waiters', '_request_task')
    
    @copy_docs(ImageHandlerBase.__new__)
    def __new__(cls):
        self = object.__new__(cls)
        self._cache = []
        self._waiters = Deque()
        self._request_task = None
        return self
    
    
    @copy_docs(ImageHandlerBase.cg_get_image)
    async def cg_get_image(self):
        cache = self._cache
        if cache:
            yield cache.pop()
            return
        
        yield None
        
        waiter = Future(KOKORO)
        self._waiters.appendleft(waiter)
        self._maybe_start_request_loop()
        yield await waiter

    
    def _maybe_start_request_loop(self):
        """
        Starts ``._request_loop`` if not yet running.
        """
        if (self._request_task is None):
            self._request_task = Task(KOKORO, self._request_loop())
    
    
    async def _request_loop(self):
        """
        Keeps requesting new image details while required.
        
        This method is a coroutine.
        """
        try:
            while self._waiters:
                details = await self._request()
                if details is None:
                    self._abort_waiters()
                    break
                
                self._feed_details(details)
                continue
        
        finally:
            self._request_task = None
    
    
    async def _request(self):
        """
        Requests a chunk of image data and processes it.
        
        This method is a coroutine
        
        Returns
        -------
        image_details : ``None | list<ImageDetailBase>``
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
        details : ``list<ImageDetailBase>``
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
