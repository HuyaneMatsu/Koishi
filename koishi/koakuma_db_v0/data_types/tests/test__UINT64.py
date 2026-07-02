from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import DATABASE_READING_ERROR_CODE_END_OF_FILE
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType

from ..uint64 import UINT64


def test__UINT64__structure():
    """
    Tests whether ``UINT64``'s structure is correct.
    """
    vampytest.assert_instance(UINT64, DataType)
    vampytest.assert_instance(UINT64.get_length, FunctionType)
    vampytest.assert_instance(UINT64.id, int)
    vampytest.assert_instance(UINT64.name, str)
    vampytest.assert_instance(UINT64.producer, FunctionType)
    vampytest.assert_instance(UINT64.reader, FunctionType)
    vampytest.assert_instance(UINT64.type_representation, type)
    vampytest.assert_instance(UINT64.type_representation_nullable, bool)
    vampytest.assert_instance(UINT64.type_representation_wrapped_into_list, bool)


async def test__UINT64__reader__good():
    """
    Tests whether ``UINT64.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good.
    """
    uint64 = 55555
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(uint64.to_bytes(8, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await UINT64.reader(data_base_reader)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, uint64)
    vampytest.assert_eq(data_base_reader.position, 8)


async def test__UINT64__reader__end_of_file():
    """
    Tests whether ``UINT64.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'nyan')
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 8),)):
        await UINT64.reader(data_base_reader)


def test__UINT64__producer():
    """
    Tests whether ``UINT64.producer`` works as intended.
    """
    uint64 = 55555
    
    parts = [*UINT64.producer(uint64)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(output, uint64.to_bytes(8, 'little'))
    

def test__UINT64__get_length():
    """
    Tests whether ``UINT64.get_length`` works as intended.
    """
    uint64 = 55555
    
    output = UINT64.get_length(uint64)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 8)
