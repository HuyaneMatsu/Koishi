from io import BytesIO

import vampytest
from scarletio import EventThread, Future, get_event_loop

from ..data_base_reader import DataBaseReader


async def test__DataBaseReader__new():
    """
    Tests whether ``DataBaseReader.__new__`` works as intended.
    
    This function is a coroutine.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    vampytest.assert_instance(data_base_reader, DataBaseReader)
    vampytest.assert_instance(data_base_reader.chunk, memoryview, nullable = True)
    vampytest.assert_instance(data_base_reader.chunk_start, int)
    vampytest.assert_instance(data_base_reader.chunk_length, int)
    vampytest.assert_instance(data_base_reader.event_loop, EventThread)
    vampytest.assert_instance(data_base_reader.position, int)
    vampytest.assert_instance(data_base_reader.future, Future, nullable = True)
    vampytest.assert_instance(data_base_reader.sync_io, object)
    
    vampytest.assert_is(data_base_reader.event_loop, event_loop)
    vampytest.assert_is(data_base_reader.sync_io, sync_io)


async def test__DataBaseReader__repr():
    """
    Tests whether ``DataBaseReader.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    
    output = repr(data_base_reader)
    vampytest.assert_instance(output, str)
