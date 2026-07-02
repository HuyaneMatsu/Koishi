from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import data_base_connected_entry_modify, DataBaseConnected

from .helpers import TestEntry


async def test__data_base_connected_entry_modify__same_length():
    """
    Tests whether ``data_base_connected_entry_modify`` works as intended.
    
    This function is a coroutine.
    
    Case: Same length.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * 50)
    start_position = 0
    end_position = 50
    entry_count_allocated = 1
    entry_count_created = 1
    entries = {}
    spaces = {}
    
    
    entry = TestEntry((20, 23, 1, 'shrimp', 517),)
    entries[entry.id] = entry
    
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
    
    output = data_base_connected_entry_modify(data_base_connected, entry, name = 'mrrrrr')
    
    vampytest.assert_instance(output, TestEntry)
    vampytest.assert_eq(output[0], 20)
    vampytest.assert_eq(output[1], 23)
    vampytest.assert_eq(output.id, entry.id)
    vampytest.assert_eq(output.name, 'mrrrrr')
    
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created)
    vampytest.assert_eq(
        data_base_connected.entries,
        {
            output.id : output,
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
                20,
                b''.join([
                    (23).to_bytes(1, 'little'),
                    (1).to_bytes(8, 'little'),
                    (6).to_bytes(1, 'little'),
                    b'mrrrrr',
                    (517).to_bytes(8, 'little'),
                ]),
            ),
        ],
    )


async def test__data_base_connected_entry_modify__different_length():
    """
    Tests whether ``data_base_connected_entry_modify`` works as intended.
    
    This function is a coroutine.
    
    Case: Different length.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * 50)
    start_position = 0
    end_position = 50
    entry_count_allocated = 1
    entry_count_created = 1
    entries = {}
    spaces = {}
    
    
    entry = TestEntry((20, 23, 1, 'shrimp', 517),)
    entries[entry.id] = entry
    
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
    
    output = data_base_connected_entry_modify(data_base_connected, entry, name = 'fry')
    
    vampytest.assert_instance(output, TestEntry)
    vampytest.assert_eq(output[0], end_position)
    vampytest.assert_eq(output[1], 20)
    vampytest.assert_eq(output.id, entry.id)
    vampytest.assert_eq(output.name, 'fry')
    
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated + 1)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created)
    vampytest.assert_eq(data_base_connected.end_position, end_position + 21)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    vampytest.assert_eq(
        data_base_connected.entries,
        {
            output.id : output,
        },
    )
    vampytest.assert_eq(
        data_base_connected.spaces,
        {
            23: [20],
        },
    )
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (
                20,
                (128 | 23).to_bytes(1, 'little'),
            ),
            (
                50,
                b''.join([
                    (20).to_bytes(1, 'little'),
                    (1).to_bytes(8, 'little'),
                    (3).to_bytes(1, 'little'),
                    b'fry',
                    (517).to_bytes(8, 'little'),
                ]),
            ),
        ],
    )
