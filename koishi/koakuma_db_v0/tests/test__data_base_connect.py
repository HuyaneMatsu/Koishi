from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..constants import DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH
from ..data_base_connected import DataBaseConnected, data_base_connect
from ..data_base_reading_error import DataBaseReadingError
from ..data_types import ENTRY_HEAD, FIELDS_DESCRIPTION, HEADER
from ..helpers import get_length_encoded_byte_count
from ..structure import get_fields_description

from .helpers import TestEntry, TestEntryDifferent


async def test__data_base_connect__good():
    """
    Tests whether ``data_base_connect`` works as intended.
    
    This function is a coroutine.
    
    Case: good.
    """
    file_path = '/tmp/test.kd'
    sync_io = BytesIO()
    
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    event_loop = get_event_loop()
    sync_io = BytesIO()
    start_position = 0
    entry_count_allocated = 3
    entry_count_created = 4
    entries = {}
    spaces = {}
    
    if start_position:
        sync_io.write(b'b' * start_position)
    
    header = (entry_count_allocated, entry_count_created)
    fields_description = get_fields_description(entry_type.__fields__)
    end_position = start_position + HEADER.get_length(header) + FIELDS_DESCRIPTION.get_length(fields_description)
    
    entry_0 = TestEntry((end_position, 23, 1, 'shrimp', 517),)
    entries[entry_0.id] = entry_0
    end_position += entry_0[1] + get_length_encoded_byte_count(entry_0[1])
    
    space_0_start = end_position
    space_0_length = 19
    spaces[space_0_length] = [space_0_start]
    end_position += space_0_length + get_length_encoded_byte_count(space_0_length)
    
    entry_1 = TestEntry((end_position, 20, 3, 'fry', 517),)
    entries[entry_1.id] = entry_1
    end_position += entry_1[1] + get_length_encoded_byte_count(entry_1[1])
    
    for part in HEADER.producer(header):
        sync_io.write(part)
    for part in FIELDS_DESCRIPTION.producer(fields_description):
        sync_io.write(part)
    
    for part in ENTRY_HEAD.producer((0, entry_0[0], entry_0[1])):
        sync_io.write(part)
    for index, field in enumerate(TestEntry.__fields__, 2):
        for part in field.data_type.producer(entry_0[index]):
            sync_io.write(part)
    
    for part in ENTRY_HEAD.producer((1, space_0_start, space_0_length)):
        sync_io.write(part)
    sync_io.write(b'a' * space_0_length)
    
    for part in ENTRY_HEAD.producer((0, entry_1[1], entry_1[1])):
        sync_io.write(part)
    for index, field in enumerate(TestEntry.__fields__, 2):
        for part in field.data_type.producer(entry_1[index]):
            sync_io.write(part)
    
    def open_sync_patched(input_file_path):
        nonlocal file_path
        nonlocal sync_io
        vampytest.assert_eq(input_file_path, file_path)
        sync_io.seek(0)
        return sync_io
    
    
    mocked = vampytest.mock_globals(
        data_base_connect,
        _open_sync = open_sync_patched,
    )
    
    output = await mocked(file_path, entry_type, start_position)
    
    vampytest.assert_instance(output, DataBaseConnected)
    
    vampytest.assert_eq(output.file_path, file_path)
    vampytest.assert_is(output.entry_type, entry_type)
    vampytest.assert_is(output.event_loop, event_loop)
    vampytest.assert_is(output.sync_io, sync_io)
    vampytest.assert_eq(output.start_position, start_position)
    vampytest.assert_eq(output.end_position, end_position)
    vampytest.assert_eq(output.entry_count_allocated, entry_count_allocated)
    vampytest.assert_eq(output.entry_count_created, entry_count_created)
    vampytest.assert_eq(output.entries, entries)
    vampytest.assert_eq(output.spaces, spaces)



async def test__data_base_connect__field_description_mismatch():
    """
    Tests whether ``data_base_connect`` works as intended.
    
    This function is a coroutine.
    
    Case: fields description mismatch.
    """
    file_path = '/tmp/test.kd'
    sync_io = BytesIO()
    
    file_path = '/tmp/test.kd'
    entry_type = TestEntry
    sync_io = BytesIO()
    start_position = 0
    entry_count_allocated = 3
    entry_count_created = 4
    
    if start_position:
        sync_io.write(b'b' * start_position)
    
    header = (entry_count_allocated, entry_count_created)
    fields_description = get_fields_description(TestEntryDifferent.__fields__)
    
    for part in HEADER.producer(header):
        sync_io.write(part)
    for part in FIELDS_DESCRIPTION.producer(fields_description):
        sync_io.write(part)
    
    def open_sync_patched(input_file_path):
        nonlocal file_path
        nonlocal sync_io
        vampytest.assert_eq(input_file_path, file_path)
        sync_io.seek(0)
        return sync_io
    
    
    mocked = vampytest.mock_globals(
        data_base_connect,
        _open_sync = open_sync_patched,
    )
    
    with vampytest.assert_raises(
        DataBaseReadingError(
            DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH,
            (fields_description, get_fields_description(entry_type.__fields__)),
        )
    ):
        await mocked(file_path, entry_type, start_position)
