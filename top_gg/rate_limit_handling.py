__all__ = ()

from hata.backend.futures import Task, ScarletLock
from hata.discord.core import KOKORO

class RateLimitContext:
    """
    Rate limit context used to handle static rate limits when communicating with top.gg.
    
    Attributes
    ----------
    acquired : `bool`
        Whether the lock is acquired.
    rate_limit_handler : ``RateLimitHandler``
        The parent rate limit handler.
    
    Usage
    -----
    ```py
    async with RateLimitContext(rate_limit_handler):
        ...
    ```
    """
    __slots__ = ('acquired', 'rate_limit_handler')
    
    def __new__(cls, rate_limit_handler):
        """
        Creates a new rate limit context instance.
        
        Parameters
        ----------
        rate_limit_handler : ``RateLimitHandler``
            The parent rate limit handler.
        """
        self = object.__new__(cls)
        self.rate_limit_handler = rate_limit_handler
        self.acquired = False
        return self
    
    
    async def __aenter__(self):
        """
        Enters the rate limit context, blocking till acquiring it.
        
        This method is a coroutine.
        """
        await self.rate_limit_handler.lock.acquire()
        self.acquired = True
        return self
    
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the rate limit context.
        
        This method is a coroutine.
        """
        self.release()
        return False
        
    
    def __del__(self):
        """Releases the rate limit context if not yet released."""
        self.release()
    
    
    def release(self):
        """Releases the rate limit context."""
        if self.acquired:
            rate_limit_handler = self.rate_limit_handler
            KOKORO.call_later(rate_limit_handler.reset_after, rate_limit_handler.lock.release)
            self.acquired = False


class StackedRateLimitHandler:
    """
    Rate limit context used to handle multiple static rate limits when communicating with top.gg.
    
    Attributes
    ----------
    acquired : `bool`
        Whether the lock is acquired.
    rate_limit_handlers : `tuple` of ``RateLimitHandler``
        The parent rate limit handlers.
    
    Usage
    -----
    ```py
    async with StackedRateLimitHandler(rate_limit_handler_1, rate_limit_handler_2):
        ...
    ```
    """
    __slots__ = ('acquired', 'rate_limit_handlers')
    
    def __new__(cls, rate_limit_handlers):
        """
        Creates a new rate limit context instance.
        
        Parameters
        ----------
        *rate_limit_handlers : ``RateLimitHandler``
            The parent rate limit handlers.
        """
        self = object.__new__(cls)
        self.rate_limit_handlers = rate_limit_handlers
        self.acquired = False
        return self
    
    
    async def __aenter__(self):
        """
        Enters the rate limit context, blocking till acquiring it.
        
        This method is a coroutine.
        """
        tasks = []
        for rate_limit_handler in self.rate_limit_handlers:
            tasks.append(Task(rate_limit_handler.lock.acquire(), KOKORO))
        
        try:
            for task in tasks:
                await task
        except:
            for rate_limit_handler, task in zip(self.rate_limit_handlers, tasks):
                if task.done():
                    rate_limit_handler.lock.release()
                else:
                    task.cancel()
            
            raise
        
        self.acquired = True
        return self
    
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the rate limit context.
        
        This method is a coroutine.
        """
        self.release()
        return False
        
    
    def __del__(self):
        """Releases the rate limit context if not yet released."""
        self.release()
    
    
    def release(self):
        """Releases the rate limit context."""
        if self.acquired:
            for rate_limit_handler in self.rate_limit_handlers:
                KOKORO.call_later(rate_limit_handler.reset_after, rate_limit_handler.lock.release)
            
            self.acquired = False


class RateLimitHandler:
    """
    Static rate limit handler implementation.
    
    Attributes
    ----------
    lock : ``ScarletLock``
        Lock used to block requests.
    reset_after : `int`
        Duration to release a rate limit after.
    """
    __slots__ = ('lock', 'reset_after', )
    
    def __new__(cls, size, reset_after):
        """
        Creates a new rate limit handler instance.
        
        Parameters
        ----------
        size : `int`
            Rate limit size.
        reset_after : `float`
            The time to reset rate limit after.
        """
        self = object.__new__(cls)
        self.reset_after = reset_after
        self.lock = ScarletLock(KOKORO, size)
        return self
