from io import BytesIO

import vampytest
from scarletio import Future, get_event_loop

from ..data_base_reader import DataBaseReader, data_base_reader_begin, data_base_reader_get_chunk


async def test__data_base_reader_get_chunk__has_more():
    """
    Tests whether ``DataBaseBegin`` works as intended.
    
    This function is a coroutine.
    
    Case: has more.
    """
    data = b'testing right?'
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
        data_base_reader_get_chunk,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    output = await mocked(data_base_reader)
    vampytest.assert_eq(output, data[:chunk_size])
    
    future = data_base_reader.future
    vampytest.assert_instance(future, Future, nullable = True)
    vampytest.assert_is_not(future, None)
    output = await future
    vampytest.assert_instance(output, bytes, nullable = True)
    vampytest.assert_is_not(output, None)
    vampytest.assert_eq(output, data[chunk_size : chunk_size << 1])
    vampytest.assert_eq(sync_io.tell(), chunk_size << 1)


async def test__data_base_reader_get_chunk__no_more():
    """
    Tests whether ``DataBaseBegin`` works as intended.
    
    This function is a coroutine.
    
    Case: no more.
    """
    data = b'tes'
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
        data_base_reader_get_chunk,
        FILE_READ_CHUNK_SIZE = chunk_size,
    )
    
    output = await mocked(data_base_reader)
    vampytest.assert_eq(output, data[:chunk_size])
    
    future = data_base_reader.future
    vampytest.assert_instance(future, Future, nullable = True)
    vampytest.assert_is(future, None)
