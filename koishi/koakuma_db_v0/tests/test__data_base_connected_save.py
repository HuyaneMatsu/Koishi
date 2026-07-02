from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import data_base_connected_save, DataBaseConnected

from .helpers import TestEntry


async def test__data_base_connected_save():
    """
    Tests whether ``data_base_connected_save`` works as intended.
    
    This function is a coroutine.
    """
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'\000' * (50 + 1 + 20))
    start_position = 0
    end_position = 50 + 1 + 20
    entry_count_allocated = 3
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
    
    space_serialised = (128 | 23).to_bytes(1, 'little')
    entry_serialised = b''.join([
        (20).to_bytes(1, 'little'),
        (1).to_bytes(8, 'little'),
        (3).to_bytes(1, 'little'),
        b'fry',
        (517).to_bytes(8, 'little'),
    ])
    
    data_base_connected.write_queue = [
        (20, space_serialised),
        (50, entry_serialised),
    ]
    
    await data_base_connected_save(data_base_connected)
    
    vampytest.assert_eq(data_base_connected.write_queue, None)
    vampytest.assert_eq(data_base_connected.end_position, end_position)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    
    sync_io.seek(start_position)
    vampytest.assert_eq(
        sync_io.read(end_position - start_position),
        b''.join([
            entry_count_allocated.to_bytes(8, 'little'),
            entry_count_created.to_bytes(8, 'little'),
            b'\000' * 4,
            space_serialised,
            b'\000' * 29,
            entry_serialised,
        ]),
    )


async def test__data_base_connected_save__end_of_file():
    """
    Tests whether ``data_base_connected_save`` works as intended.
    
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
    entry_count_allocated = 3
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
    end_position += 1 + 20
    data_base_connected.end_position = end_position
    
    space_serialised = (128 | 23).to_bytes(1, 'little')
    entry_serialised = b''.join([
        (20).to_bytes(1, 'little'),
        (1).to_bytes(8, 'little'),
        (3).to_bytes(1, 'little'),
        b'fry',
        (517).to_bytes(8, 'little'),
    ])
    
    data_base_connected.write_queue = [
        (20, space_serialised),
        (50, entry_serialised),
    ]
    
    await data_base_connected_save(data_base_connected)
    
    vampytest.assert_eq(data_base_connected.write_queue, None)
    vampytest.assert_eq(data_base_connected.end_position, end_position)
    vampytest.assert_eq(data_base_connected.end_position_real, end_position)
    
    sync_io.seek(start_position)
    vampytest.assert_eq(
        sync_io.read(end_position - start_position),
        b''.join([
            entry_count_allocated.to_bytes(8, 'little'),
            entry_count_created.to_bytes(8, 'little'),
            b'\000' * 4,
            space_serialised,
            b'\000' * 29,
            entry_serialised,
        ]),
    )
