from io import BytesIO

import vampytest
from scarletio import get_event_loop

from ..data_base_reader import DataBaseReader, data_base_reader_begin, data_base_reader_abort


async def test__data_base_reader_abort__began():
    """
    Tests whether ``data_base_reader_abort`` works as intended.
    
    This function is a coroutine.
    
    Case: began.
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
    
    data_base_reader_abort(data_base_reader)
    vampytest.assert_is(data_base_reader.chunk, None)
    vampytest.assert_is(data_base_reader.future, None)


async def test__data_base_reader_abort__not_running():
    """
    Tests whether ``data_base_reader_abort`` works as intended.
    
    This function is a coroutine.
    
    Case: began.
    """
    data = b'testing'
    chunk_size = 4
    sync_io = BytesIO()
    sync_io.write(data)
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    data_base_reader_abort(data_base_reader)
    vampytest.assert_is(data_base_reader.chunk, None)
    vampytest.assert_is(data_base_reader.future, None)
