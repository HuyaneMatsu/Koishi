from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..constants import (
    DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE, DATABASE_READING_ERROR_CODE_END_OF_FILE
)
from ..data_base_reader import DataBaseReader, data_base_reader_begin
from ..data_base_reading_error import DataBaseReadingError
from ..data_types import STRING
from ..helpers import read_length



async def test__read_length__good_zero_length():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, nulled.
    """
    sync_io = BytesIO()
    sync_io.write((0).to_bytes(1, 'little'))
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await read_length(data_base_reader, STRING)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__read_length__good_regular_length():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, regular length.
    """
    sync_io = BytesIO()
    sync_io.write((5).to_bytes(1, 'little'))
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await read_length(data_base_reader, STRING)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 5)
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__read_length__good_extended_length():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, extended length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((64 | 2).to_bytes(1, 'little'))
    sync_io.write((256).to_bytes(2, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await read_length(data_base_reader, STRING)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 256)
    vampytest.assert_eq(data_base_reader.position, 3)


async def test__read_length__end_of_file_reading_length():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 1),)):
        await read_length(data_base_reader, STRING)


async def test__read_length__end_of_file_reading_extended_length():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading extended length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((64 | 2).to_bytes(1, 'little'))
    sync_io.write(b'a')
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (1, 2),)):
        await read_length(data_base_reader, STRING)


async def test__read_length__extended_length_byte_count_out_of_range():
    """
    Tests whether ``read_length`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading extended length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((64 | 9).to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(
        DataBaseReadingError(DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE, (1, STRING, 9),)
    ):
        await read_length(data_base_reader, STRING)
