__all__ = ('end_remind_loop', 'start_remind_loop')

from hata import KOKORO

from .reminding import remind_forgot_daily


REMIND_INTERVAL = 30 * 60 # half hour

handle = None


def end_remind_loop():
    """
    Ends the remind loop.
    """
    global handle
    if handle is None:
        return
    
    handle.cancel()
    handle = None


def start_remind_loop():
    """
    Begins the remind loop.
    """
    global handle
    if handle is not None:
        return
    
    step_remind_loop()


def step_remind_loop():
    """
    Steps the remind loop.
    """
    global handle
    handle = KOKORO.call_after(REMIND_INTERVAL, step_remind_loop)
    KOKORO.create_task(remind_forgot_daily())
