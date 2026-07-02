from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import DATABASE_READING_ERROR_CODE_END_OF_FILE
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType

from ..entry_id import ENTRY_ID


def test__ENTRY_ID__structure():
    """
    Tests whether ``ENTRY_ID``'s structure is correct.
    """
    vampytest.assert_instance(ENTRY_ID, DataType)
    vampytest.assert_instance(ENTRY_ID.get_length, FunctionType)
    vampytest.assert_instance(ENTRY_ID.id, int)
    vampytest.assert_instance(ENTRY_ID.name, str)
    vampytest.assert_instance(ENTRY_ID.producer, FunctionType)
    vampytest.assert_instance(ENTRY_ID.reader, FunctionType)
    vampytest.assert_instance(ENTRY_ID.type_representation, type)
    vampytest.assert_instance(ENTRY_ID.type_representation_nullable, bool)
    vampytest.assert_instance(ENTRY_ID.type_representation_wrapped_into_list, bool)


async def test__ENTRY_ID__reader__good():
    """
    Tests whether ``ENTRY_ID.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good.
    """
    entry_id = 55555
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(entry_id.to_bytes(8, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_ID.reader(data_base_reader)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, entry_id)
    vampytest.assert_eq(data_base_reader.position, 8)


async def test__ENTRY_ID__reader__end_of_file():
    """
    Tests whether ``ENTRY_ID.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file.
    """
    sync_io = BytesIO()
    event_loop = get_event_loop()
    sync_io.write(b'nyan')
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 8),)):
        await ENTRY_ID.reader(data_base_reader)


def test__ENTRY_ID__producer():
    """
    Tests whether ``ENTRY_ID.producer`` works as intended.
    """
    entry_id = 55555
    
    parts = [*ENTRY_ID.producer(entry_id)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(output, entry_id.to_bytes(8, 'little'))
    

def test__ENTRY_ID__get_length():
    """
    Tests whether ``ENTRY_ID.get_length`` works as intended.
    """
    entry_id = 55555
    
    output = ENTRY_ID.get_length(entry_id)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 8)
