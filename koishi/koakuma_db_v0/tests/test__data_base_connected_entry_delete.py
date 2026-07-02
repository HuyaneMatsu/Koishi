from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import data_base_connected_entry_delete, DataBaseConnected

from .helpers import TestEntry


async def test__data_base_connected_entry_delete():
    """
    Tests whether ``data_base_connected_entry_delete`` works as intended.
    
    This function is a coroutine.
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
    
    data_base_connected_entry_delete(data_base_connected, entry)
    
    vampytest.assert_eq(data_base_connected.entry_count_allocated, entry_count_allocated)
    vampytest.assert_eq(data_base_connected.entry_count_created, entry_count_created)
    vampytest.assert_eq(data_base_connected.end_position, end_position)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    vampytest.assert_eq(
        data_base_connected.entries,
        {},
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
        ],
    )
