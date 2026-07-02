from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..constants import DATABASE_READING_ERROR_CODE_END_OF_FILE
from ..data_base_reader import DataBaseReader, data_base_reader_begin, data_base_reader_skip
from ..data_base_reading_error import DataBaseReadingError


async def test__data_base_reader_skip__can_read():
    """
    Tests whether ``data_base_reader_skip`` works as intended.
    
    This function is a coroutine.
    
    Case: can read.
    """
    data = b'testing'
    chunk_size = 4
    sync_io = BytesIO()
    sync_io.write(data)
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    mocked = vampytest.mock_globals(
        data_base_reader_begin,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    mocked(data_base_reader, 0)
    
    mocked = vampytest.mock_globals(
        data_base_reader_skip,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    output = await mocked(data_base_reader, 3)
    vampytest.assert_is(output, None)
    
    vampytest.assert_eq(data_base_reader.position, 3)
    vampytest.assert_eq(data_base_reader.chunk_start, 3)
    vampytest.assert_eq(data_base_reader.chunk_length, 4)
    vampytest.assert_eq(data_base_reader.chunk, b'test')
    
    output = await mocked(data_base_reader, 3)
    vampytest.assert_is(output, None)
    
    vampytest.assert_eq(data_base_reader.position, 6)
    vampytest.assert_eq(data_base_reader.chunk_start, 2)
    vampytest.assert_eq(data_base_reader.chunk_length, 3)
    vampytest.assert_eq(data_base_reader.chunk, b'ing')
    

async def test__data_base_reader_skip__over_read_single_chunk():
    """
    Tests whether ``data_base_reader_skip`` works as intended.
    
    This function is a coroutine.
    
    Case: over read - single chunk.
    """
    data = b'testing'
    chunk_size = 10
    sync_io = BytesIO()
    sync_io.write(data)
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    mocked = vampytest.mock_globals(
        data_base_reader_begin,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    mocked(data_base_reader, 0)
    
    mocked = vampytest.mock_globals(
        data_base_reader_skip,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 10))):
        await mocked(data_base_reader, 10)
    
    vampytest.assert_is(data_base_reader.chunk, None)
    vampytest.assert_is(data_base_reader.future, None)


async def test__data_base_reader_skip__over_read_multiple_chunks():
    """
    Tests whether ``data_base_reader_skip`` works as intended.
    
    This function is a coroutine.
    
    Case: Over read, multiple chunks.
    """
    data = b'testing'
    chunk_size = 4
    sync_io = BytesIO()
    sync_io.write(data)
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    mocked = vampytest.mock_globals(
        data_base_reader_begin,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    mocked(data_base_reader, 0)
    
    mocked = vampytest.mock_globals(
        data_base_reader_skip,
        2,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 10))):
        await mocked(data_base_reader, 10)
    
    
    vampytest.assert_is(data_base_reader.chunk, None)
    vampytest.assert_is(data_base_reader.future, None)
