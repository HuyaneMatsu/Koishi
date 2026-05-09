from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from types import FunctionType

import vampytest
from scarletio import TimerHandle, skip_ready_cycle

from ..looper import ReminderLooper


def _assert_fields_set(reminder_looper):
    """
    Tests whether ``ReminderLooper`` works as intended.
    
    Parameters
    ----------
    reminder_looper : ``ReminderLooper``
        Reminder to test.
    """
    vampytest.assert_instance(reminder_looper, ReminderLooper)
    vampytest.assert_instance(reminder_looper.entries_getter, FunctionType)
    vampytest.assert_instance(reminder_looper.handle, TimerHandle, nullable = True)
    vampytest.assert_instance(reminder_looper.interval_default, float)
    vampytest.assert_instance(reminder_looper.interval_getter, FunctionType, nullable = True)
    vampytest.assert_instance(reminder_looper.location, str)
    vampytest.assert_instance(reminder_looper.notifier, FunctionType)
    vampytest.assert_instance(reminder_looper.running, bool)


def test__ReminderLooper__new():
    """
    Tests whether ``ReminderLooper.__new__`` works intended.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    async def interval_getter(input_interval_default):
        return input_interval_default
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
        interval_getter = interval_getter,
    )
    _assert_fields_set(reminder_looper)
    
    vampytest.assert_is(reminder_looper.entries_getter, entries_getter)
    vampytest.assert_is(reminder_looper.handle, None)
    vampytest.assert_eq(reminder_looper.interval_default, interval_default)
    vampytest.assert_eq(reminder_looper.location, location)
    vampytest.assert_is(reminder_looper.notifier, notifier)
    vampytest.assert_eq(reminder_looper.running, False)


async def test__ReminderLooper__start__not_yet_started():
    """
    Tests whether ``ReminderLooper.start`` works as intended.
    
    This function is a coroutine.
    
    Case: Not yet started.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    
    step_remind_loop_called = False
    
    async def step(self):
        nonlocal step_remind_loop_called
        step_remind_loop_called = True
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    
    step_original = ReminderLooper.step
    ReminderLooper.step = step
    
    try:
        reminder_looper.start()
    finally:
        ReminderLooper.step = step_original
    
    try:
        await skip_ready_cycle()
        
        vampytest.assert_true(step_remind_loop_called)
        vampytest.assert_eq(reminder_looper.running, True)
    
    finally:
        reminder_looper.stop()


async def test__ReminderLooper__start__already_started():
    """
    Tests whether ``ReminderLooper.start`` works as intended.
    
    This function is a coroutine.
    
    Case: Already started.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    
    step_remind_loop_called = False
    
    async def step(self):
        nonlocal step_remind_loop_called
        step_remind_loop_called = True
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.running = True
    reminder_looper.handle = TimerHandle(0.0, lambda : None, ())
    
    step_original = ReminderLooper.step
    ReminderLooper.step = step
    
    try:
        reminder_looper.start()
    finally:
        ReminderLooper.step = step_original
    
    try:
        await skip_ready_cycle()
        
        vampytest.assert_false(step_remind_loop_called)
    
    finally:
        reminder_looper.stop()


async def test__ReminderLooper__step():
    """
    Tests whether ``ReminderLooper.step`` works as intended.
    
    This function is a coroutine.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    execute_remind_called = False
    
    async def execute_remind(input_location, input_entries_getter, input_notifier):
        nonlocal location
        nonlocal entries_getter
        nonlocal notifier
        nonlocal execute_remind_called
        vampytest.assert_eq(input_location, location)
        vampytest.assert_eq(input_entries_getter, entries_getter)
        vampytest.assert_eq(input_notifier, notifier)
        execute_remind_called = True
        
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.running = True
    reminder_looper.handle = TimerHandle(0.0, lambda : None, ())
    
    step = vampytest.mock_globals(
        ReminderLooper.step,
        execute_remind = execute_remind,
    )
    
    try:
        await step(reminder_looper)
    
    finally:
        handle = reminder_looper.handle
        if (handle is not None):
            handle.cancel()
            handle = None
    
    await skip_ready_cycle()
    vampytest.assert_true(execute_remind_called)


def test__ReminderLooper__stop__not_yet_ended():
    """
    Tests whether ``ReminderLooper.stop`` works as intended.
    
    Case: Not yet stopped.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.running = True
    reminder_looper.handle = handle = TimerHandle(0.0, lambda : None, ())
    
    try:
        reminder_looper.stop()
        
        vampytest.assert_eq(reminder_looper.running, False)
        vampytest.assert_true(handle.cancelled)
    
    finally:
        handle.cancel()
        handle = None


def test__ReminderLooper__stop__already_stopped():
    """
    Tests whether ``ReminderLooper.stop`` works as intended.
    
    Case: Already stopped.
    """
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    
    reminder_looper.stop()
    vampytest.assert_eq(reminder_looper.running, False)
    vampytest.assert_is(reminder_looper.handle, None)


def test__ensure_step_at_date_time__not_started():
    """
    Tests whether ``ReminderLooper.ensure_step_at_date_time`` works as intended.
    
    Case: Not started.
    """
    now = DateTime.now(TimeZone.utc)
    
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    
    reminder_looper.ensure_step_at_date_time(now + TimeDelta(seconds = 60.0))
    vampytest.assert_is(reminder_looper.handle, None)


def test__ensure_step_at_date_time__started_in_step():
    """
    Tests whether ``ReminderLooper.ensure_step_at_date_time`` works as intended.
    
    Case: Started, in step.
    """
    now = DateTime.now(TimeZone.utc)
    
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 0.0001
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.running = True
    
    handle = None
    try:
        reminder_looper.ensure_step_at_date_time(now + TimeDelta(seconds = 60.0))
        handle = reminder_looper.handle
        vampytest.assert_is_not(handle, None)
        vampytest.assert_instance(handle, TimerHandle)
    
    finally:
        if (handle is not None):
            handle.cancel()
            handle = None
        
        reminder_looper.running = False


async def test__ensure_step_at_date_time__started_further():
    """
    Tests whether ``ReminderLooper.ensure_step_at_date_time`` works as intended.
    
    This function is a coroutine.
    
    Case: Started, further.
    """
    now = DateTime.now(TimeZone.utc)
    
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 60.0
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.start()
        
    try:
        await skip_ready_cycle()
        
        handle = reminder_looper.handle
        vampytest.assert_is_not(handle, None)
        vampytest.assert_instance(handle, TimerHandle)
        handle.cancel()
        
        old_handle = reminder_looper.handle
        vampytest.assert_is_not(handle, None)
        vampytest.assert_instance(handle, TimerHandle)
        
        
        reminder_looper.ensure_step_at_date_time(now + TimeDelta(seconds = 30.0))
        
        new_handle = reminder_looper.handle
        vampytest.assert_is_not(new_handle, None)
        vampytest.assert_instance(new_handle, TimerHandle)
        
        vampytest.assert_is_not(old_handle, new_handle)
        vampytest.assert_true(old_handle.cancelled)
    
    finally:
        reminder_looper.stop()


async def test__ensure_step_at_date_time__started_closer():
    """
    Tests whether ``ReminderLooper.ensure_step_at_date_time`` works as intended.
    
    This function is a coroutine.
    
    Case: Started, closer.
    """
    now = DateTime.now(TimeZone.utc)
    
    location = 'hell'
    
    async def entries_getter(input_connector):
        return []
    
    async def notifier(entry):
        return True
    
    interval_default = 60
    
    reminder_looper = ReminderLooper(
        location,
        entries_getter,
        notifier,
        interval_default = interval_default,
    )
    reminder_looper.start()
    
    try:
        await skip_ready_cycle()
        
        old_handle = reminder_looper.handle
        vampytest.assert_is_not(old_handle, None)
        vampytest.assert_instance(old_handle, TimerHandle)
        
        
        reminder_looper.ensure_step_at_date_time(now + TimeDelta(seconds = 90.0))
        
        new_handle = reminder_looper.handle
        vampytest.assert_is_not(new_handle, None)
        vampytest.assert_instance(new_handle, TimerHandle)
        
        vampytest.assert_is(old_handle, new_handle)
        vampytest.assert_false(old_handle.cancelled)
    
    finally:
        reminder_looper.stop()
