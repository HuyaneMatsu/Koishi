from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import DATABASE_READING_ERROR_CODE_END_OF_FILE
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType

from ..header import HEADER


def test__HEADER__structure():
    """
    Tests whether ``HEADER``'s structure is correct.
    """
    vampytest.assert_instance(HEADER, DataType)
    vampytest.assert_instance(HEADER.get_length, FunctionType)
    vampytest.assert_instance(HEADER.id, int)
    vampytest.assert_instance(HEADER.name, str)
    vampytest.assert_instance(HEADER.producer, FunctionType)
    vampytest.assert_instance(HEADER.reader, FunctionType)
    vampytest.assert_instance(HEADER.type_representation, type)
    vampytest.assert_instance(HEADER.type_representation_nullable, bool)
    vampytest.assert_instance(HEADER.type_representation_wrapped_into_list, bool)


async def test__HEADER__reader__good():
    """
    Tests whether ``HEADER.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good.
    """
    entry_count_allocated = 55555
    entry_count_created = 422
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(entry_count_allocated.to_bytes(8, 'little'))
    sync_io.write(entry_count_created.to_bytes(8, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await HEADER.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (entry_count_allocated, entry_count_created))
    vampytest.assert_eq(data_base_reader.position, 16)


async def test__HEADER__reader__end_of_file():
    """
    Tests whether ``HEADER.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 16),)):
        await HEADER.reader(data_base_reader)


def test__HEADER__producer():
    """
    Tests whether ``HEADER.producer`` works as intended.
    """
    entry_count_allocated = 55555
    entry_count_created = 422
    
    parts = [*HEADER.producer((entry_count_allocated, entry_count_created))]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            entry_count_allocated.to_bytes(8, 'little'),
            entry_count_created.to_bytes(8, 'little'),
        ])
    )
    

def test__HEADER__get_length():
    """
    Tests whether ``HEADER.get_length`` works as intended.
    """
    entry_count_allocated = 55555
    entry_count_created = 422
    
    output = HEADER.get_length((entry_count_allocated, entry_count_created))
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 16)
