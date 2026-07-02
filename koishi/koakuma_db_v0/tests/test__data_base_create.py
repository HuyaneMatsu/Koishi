from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_connected import DataBaseConnected, data_base_create
from ..data_types import FIELDS_DESCRIPTION, HEADER
from ..structure import get_fields_description

from .helpers import TestEntry


async def test__data_base_create():
    """
    Tests whether ``data_base_create`` works as intended.
    
    This function is a coroutine.
    """
    file_path = '/tmp/test.kd'
    sync_io = BytesIO()
    
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    start_position = 0
    
    if start_position:
        sync_io.write(b'b' * start_position)
    
    header = (0, 0)
    fields_description = get_fields_description(entry_type.__fields__)
    end_position = start_position + HEADER.get_length(header) + FIELDS_DESCRIPTION.get_length(fields_description)
    
    def open_and_write_initial_data_sync_patched(input_file_path, input_position, initial_data):
        nonlocal file_path
        nonlocal sync_io
        nonlocal start_position
        vampytest.assert_eq(input_file_path, file_path)
        vampytest.assert_eq(input_position, start_position)
        sync_io.seek(0)
        sync_io.write(initial_data)
        return sync_io
    
    
    mocked = vampytest.mock_globals(
        data_base_create,
        _open_and_write_initial_data_sync = open_and_write_initial_data_sync_patched,
    )
    
    output = await mocked(file_path, entry_type, start_position)
    
    vampytest.assert_instance(output, DataBaseConnected)
    
    vampytest.assert_eq(output.file_path, file_path)
    vampytest.assert_is(output.entry_type, entry_type)
    vampytest.assert_is(output.event_loop, event_loop)
    vampytest.assert_is(output.sync_io, sync_io)
    vampytest.assert_eq(output.start_position, start_position)
    vampytest.assert_eq(output.end_position, end_position)
    vampytest.assert_eq(output.entry_count_allocated, 0)
    vampytest.assert_eq(output.entry_count_created, 0)
    vampytest.assert_eq(output.entries, {})
    vampytest.assert_eq(output.spaces, {})
    
    sync_io.seek(start_position)
    
    vampytest.assert_eq(
        sync_io.read(end_position - start_position),
        b''.join([*HEADER.producer(header), *FIELDS_DESCRIPTION.producer(fields_description)]),
    )
