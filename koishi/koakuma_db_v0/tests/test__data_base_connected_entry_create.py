from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import data_base_connected_entry_create, data_base_connected_entry_delete, DataBaseConnected

from .helpers import TestEntry


async def test__data_base_connected_entry_create():
    """
    Tests whether ``data_base_connected_entry_create`` works as intended.
    
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
    entry_count_created = 1
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
    
    entry = data_base_connected_entry_create(data_base_connected, name = 'shrimp', value = 517)
    
    vampytest.assert_instance(entry, TestEntry)
    vampytest.assert_eq(entry.id, entry_count_created + 1)
    vampytest.assert_eq(entry.name, 'shrimp')
    vampytest.assert_eq(entry.value, 517)
    
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated + 1)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created + 1)
    vampytest.assert_eq(data_base_connected.end_position, end_position + 24)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    vampytest.assert_eq(
        data_base_connected.entries,
        {
            entry.id : entry,
        },
    )
    vampytest.assert_eq(
        data_base_connected.spaces,
        {},
    )
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (
                end_position,
                b''.join([
                    (23).to_bytes(1, 'little'),
                    (entry_count_created + 1).to_bytes(8, 'little'),
                    (6).to_bytes(1, 'little'),
                    b'shrimp',
                    (517).to_bytes(8, 'little'),
                ]),
            ),
        ],
    )


async def test__data_base_connected_entry_create__delete_after():
    """
    Tests whether ``data_base_connected_entry_create`` works as intended.
    
    This function is a coroutine.
    
    Case: delete after; should adjust the fill length to match the entry length.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * 50)
    start_position = 0
    end_position = 50
    entry_count_allocated = 0
    entry_count_created = 1
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
    
    entry = data_base_connected_entry_create(data_base_connected, name = 'shrimp', value = 517)
    data_base_connected_entry_delete(data_base_connected, entry)
    
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated + 1)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created + 1)
    vampytest.assert_eq(data_base_connected.end_position, end_position + 24)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    vampytest.assert_eq(
        data_base_connected.entries,
        {},
    )
    vampytest.assert_eq(
        data_base_connected.spaces,
        {
            23 : [end_position]
        },
    )
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (
                end_position,
                b''.join([
                    (128 | 23).to_bytes(1, 'little'),
                    b'\000' * 23,
                ]),
            ),
        ],
    )
