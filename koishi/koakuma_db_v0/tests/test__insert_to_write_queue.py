from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import _insert_to_write_queue, DataBaseConnected

from .helpers import TestEntry


async def test__insert_to_write_queue__new():
    """
    Tests whether ``_insert_to_write_queue`` works as intended.
    
    This function is a coroutine.
    
    Case: new.
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
    
    _insert_to_write_queue(data_base_connected, 20, b'nyan')
    
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (20, b'nyan'),
        ],
    )


async def test__insert_to_write_queue__existing():
    """
    Tests whether ``_insert_to_write_queue`` works as intended.
    
    This function is a coroutine.
    
    Case: existing.
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
    
    data_base_connected.write_queue = [
        (10, b'rawr'),
        (20, b'pyon'),
        (30, b'awoo'),
    ]
    
    _insert_to_write_queue(data_base_connected, 20, b'nyan')
    
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (10, b'rawr'),
            (20, b'nyan'),
            (30, b'awoo'),
        ],
    )
