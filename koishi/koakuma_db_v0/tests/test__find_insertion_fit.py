from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import _find_insertion_fit, DataBaseConnected

from .helpers import TestEntry


async def test__find_insertion_fit__no_space():
    """
    Tests whether ``_find_insertion_fit`` works as intended.
    
    This function is a coroutine.
    
    Case: no space.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * 50)
    start_position = 0
    end_position = 50
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
    
    header_length = 1
    entry_length = 10
    
    output = _find_insertion_fit(data_base_connected, header_length, entry_length)
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, end_position)
    
    vampytest.assert_eq(data_base_connected.end_position, end_position + header_length + entry_length)
    vampytest.assert_eq(data_base_connected.spaces, {})


async def test__find_insertion_fit__matches_space():
    """
    Tests whether ``_find_insertion_fit`` works as intended.
    
    This function is a coroutine.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * 50)
    start_position = 0
    end_position = 50
    entry_count_allocated = 0
    entry_count_created = 0
    entries = {}
    spaces = {
        10 : [20],
    }
    
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
    
    header_length = 1
    entry_length = 10
    
    output = _find_insertion_fit(data_base_connected, header_length, entry_length)
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 20)
    
    vampytest.assert_eq(data_base_connected.end_position, end_position)
    vampytest.assert_eq(data_base_connected.spaces, {})
