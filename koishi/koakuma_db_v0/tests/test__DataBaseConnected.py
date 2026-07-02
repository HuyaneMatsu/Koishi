from io import BytesIO

import vampytest
from scarletio import EventThread, get_event_loop

from ..data_base_connected import DataBaseConnected
from ..structure import EntryStructure

from .helpers import TestEntry


async def test__DataBaseConnected__new():
    """
    Tests whether ``DataBaseConnected.__new__`` works as intended.
    
    This function is a coroutine.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    start_position = 0
    end_position = 0
    entry_count_allocated = 0
    entry_count_created = 0
    entries = {}
    spaces = {}
    
    data_base_connected = DataBaseConnected(
        file_path,
        entry_type,
        event_loop,
        sync_io,
        start_position,
        end_position,
        entry_count_allocated,
        entry_count_created,
        entries,
        spaces,
    )
    
    vampytest.assert_instance(data_base_connected, DataBaseConnected)
    vampytest.assert_instance(data_base_connected.end_position, int)
    vampytest.assert_instance(data_base_connected.end_position_real, int)
    vampytest.assert_instance(data_base_connected.entries, dict)
    vampytest.assert_instance(data_base_connected.entry_count_allocated, int)
    vampytest.assert_instance(data_base_connected.entry_count_created, int)
    vampytest.assert_instance(data_base_connected.entry_type, EntryStructure)
    vampytest.assert_instance(data_base_connected.event_loop, EventThread)
    vampytest.assert_instance(data_base_connected.file_path, str)
    vampytest.assert_instance(data_base_connected.spaces, dict)
    vampytest.assert_instance(data_base_connected.start_position, int)
    vampytest.assert_instance(data_base_connected.sync_io, type(sync_io))
    vampytest.assert_instance(data_base_connected.write_queue, list, nullable = True)
    
    vampytest.assert_eq(data_base_connected.end_position, end_position)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    vampytest.assert_eq(data_base_connected.entries, entries)
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created)
    vampytest.assert_is(data_base_connected.entry_type, entry_type)
    vampytest.assert_is(data_base_connected.event_loop, event_loop)
    vampytest.assert_eq(data_base_connected.file_path, file_path)
    vampytest.assert_eq(data_base_connected.spaces, spaces)
    vampytest.assert_eq(data_base_connected.start_position, start_position)
    vampytest.assert_is(data_base_connected.sync_io, sync_io)
    vampytest.assert_is(data_base_connected.write_queue, None)


async def test__DataBaseConnected__repr():
    """
    Tests whether ``DataBaseConnected.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    start_position = 0
    end_position = 0
    entry_count_allocated = 0
    entry_count_created = 0
    entries = {}
    spaces = {}
    
    data_base_connected = DataBaseConnected(
        file_path,
        entry_type,
        event_loop,
        sync_io,
        start_position,
        end_position,
        entry_count_allocated,
        entry_count_created,
        entries,
        spaces,
    )
    
    output = repr(data_base_connected)
    vampytest.assert_instance(output, str)
