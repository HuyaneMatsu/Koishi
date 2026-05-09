__all__ = ('ReminderLooper',)

from datetime import datetime as DateTime, timezone as TimeZone
from time import monotonic

from hata import KOKORO
from scarletio import RichAttributeErrorBaseType, Task

from config import MARISA_MODE

from .reminding import execute_remind, request_interval


REMIND_INTERVAL = 30 * 60 # half hour
if MARISA_MODE:
    REMIND_INTERVAL /= 60


class ReminderLooper(RichAttributeErrorBaseType):
    """
    Base type to loop a reminder.
    
    Attributes
    ----------
    entries_getter : `CoroutineFunctionType`
        A function to get the entries to be reminded.
    
    handle : ``None | TimerHandle``
        Ensured handle on the event loop.
    
    interval_getter : `None | CoroutineFunctionType`
        Function to get the amount of time till next call.
    
    interval_default : `float`
        The amount of seconds between runs.
    
    location : `str`
        Location name to use for exception handler.
    
    notifier : `CoroutineFunctionType`
        Notifier function.
    
    running : `bool`
        Whether the looper is currently running.
    """
    __slots__ = ('entries_getter', 'handle', 'interval_default', 'interval_getter', 'location', 'notifier', 'running')
    
    
    def __new__(
        cls, location, entries_getter, notifier, *, interval_default = REMIND_INTERVAL, interval_getter = None):
        """
        Creates a new reminder looper.
        
        Parameters
        ----------
        location : `str`
            Location name to use for exception handler.
        
        entries_getter : `CoroutineFunctionType`
            A function to get the entries to be reminded.
        
        notifier : ``CoroutineFunctionType`
            Notifier function.
        
        interval_default : `float` = `REMIND_INTERVAL`, Optional (Keyword only)
            The amount of seconds between runs.
        
        interval_getter : `None | CoroutineFunctionType`, Optional (Keyword only)
            Function to get the amount of time till next call.
        """
        self = object.__new__(cls)
        self.entries_getter = entries_getter
        self.handle = None
        self.interval_default = interval_default
        self.interval_getter = interval_getter
        self.location = location
        self.notifier = notifier
        self.running = False
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # location
        repr_parts.append(' location = ')
        repr_parts.append(repr(self.location))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def stop(self):
        """
        Ends the remind loop.
        """
        self.running = False
        
        handle = self.handle
        if (handle is not None):
            self.handle = None
            handle.cancel()
    
    
    def start(self):
        """
        Begins the remind loop.
        """
        if self.running:
            return
        
        self.running = True
        
        if (self.handle is None):
            Task(KOKORO, self.step())
    
    
    def ensure_step_at_date_time(self, date_time):
        """
        Ff the given date time is earlier than the current step, ensures that the step's occurrence is set to it.
        
        Parameters
        ----------
        date_time : ``DateTime``
            Date time to check.
        """
        if not self.running:
            return
        
        expected_occurrence = monotonic() + (date_time - DateTime.now(TimeZone.utc)).total_seconds()
        handle = self.handle
        
        while True:
            if (handle is not None):
                if handle.when <= expected_occurrence:
                    break
                
                handle.cancel()
            
            self.handle = KOKORO.call_at(expected_occurrence, _execute_step, self)
            break
    
    
    async def step(self):
        """
        Steps the remind loop.
        
        This function is a coroutine.
        """
        # Set the current handle to `None`, so we can make sure not to overwrite it.
        handle = self.handle
        if (handle is not None):
            self.handle = None
            handle.cancel()
        
        interval = self.interval_default
        try:
            await execute_remind(self.location, self.entries_getter, self.notifier)
            
            interval = await request_interval(self.location, interval, self.interval_getter)
        finally:
            if self.running:
                while True:
                    handle = self.handle
                    expected_occurrence = monotonic() + interval
                    if (handle is not None):
                        if handle.when <= expected_occurrence:
                            break
                        
                        handle.cancel()
                    
                    self.handle = KOKORO.call_at(expected_occurrence, _execute_step, self)
                    break


def _execute_step(looper):
    """
    Begins executing a looper step.
    
    Parameters
    ----------
    looper : ``ReminderLooper``
    """
    Task(KOKORO, looper.step())
