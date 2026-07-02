from io import BytesIO

import vampytest
from scarletio import Future, get_event_loop

from ..data_base_reader import DataBaseReader, data_base_reader_begin


async def test__data_base_reader_begin():
    """
    Tests whether ``data_base_reader_begin`` works as intended.
    
    This function is a coroutine.
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
    future = data_base_reader.future
    vampytest.assert_instance(future, Future, nullable = True)
    vampytest.assert_is_not(future, None)
    output = await future
    vampytest.assert_instance(output, bytes, nullable = True)
    vampytest.assert_is_not(output, None)
    vampytest.assert_eq(output, data[:chunk_size])
    vampytest.assert_eq(sync_io.tell(), chunk_size)
