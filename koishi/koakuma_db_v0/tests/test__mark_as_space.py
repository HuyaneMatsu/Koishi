from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import _mark_as_space, DataBaseConnected

from .helpers import TestEntry


async def test__mark_as_space():
    """
    Tests whether ``_mark_as_space`` works as intended.
    
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
    
    _mark_as_space(data_base_connected, 20, 10)
    
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (20, (128 | 10).to_bytes(1, 'little')),
        ],
    )
    vampytest.assert_eq(
        spaces,
        {
            10: [20],
        },
    )


async def test__mark_as_space__end_of_file():
    """
    Tests whether ``_mark_as_space`` works as intended.
    
    This function is a coroutine.
    
    Case: end of file.
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
    
    _mark_as_space(data_base_connected, 50, 10)
    
    vampytest.assert_eq(
        data_base_connected.write_queue,
        [
            (
                50,
                b''.join([
                    (128 | 10).to_bytes(1, 'little'),
                    b'\000' * 10,
                ]),
            ),
        ],
    )
    vampytest.assert_eq(
        spaces,
        {
            10: [50],
        },
    )
