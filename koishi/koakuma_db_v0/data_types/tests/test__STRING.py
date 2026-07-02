from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import (
    DATABASE_READING_ERROR_CODE_END_OF_FILE, DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE
)
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType

from ..string import STRING


def test__STRING__structure():
    """
    Tests whether ``STRING``'s structure is correct.
    """
    vampytest.assert_instance(STRING, DataType)
    vampytest.assert_instance(STRING.get_length, FunctionType)
    vampytest.assert_instance(STRING.id, int)
    vampytest.assert_instance(STRING.name, str)
    vampytest.assert_instance(STRING.producer, FunctionType)
    vampytest.assert_instance(STRING.reader, FunctionType)
    vampytest.assert_instance(STRING.type_representation, type)
    vampytest.assert_instance(STRING.type_representation_nullable, bool)
    vampytest.assert_instance(STRING.type_representation_wrapped_into_list, bool)


async def test__STRING__reader__good_nulled():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, nulled.
    """
    string = None
    sync_io = BytesIO()
    sync_io.write((0).to_bytes(1, 'little'))
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await STRING.reader(data_base_reader)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, string)
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__STRING__reader__good_regular_length():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, regular length.
    """
    string = 'ayaya'
    sync_io = BytesIO()
    sync_io.write((5).to_bytes(1, 'little'))
    sync_io.write(string.encode())
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await STRING.reader(data_base_reader)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, string)
    vampytest.assert_eq(data_base_reader.position, 6)


async def test__STRING__reader__good_regular_length_unicode():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, regular length, unicode.
    """
    string = 'űűűűű'
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((10).to_bytes(1, 'little'))
    sync_io.write(string.encode())
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await STRING.reader(data_base_reader)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, string)
    vampytest.assert_eq(data_base_reader.position, 11)


async def test__STRING__reader__good_extended_length():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, extended length.
    """
    string = 'a' * 256
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((64 | 2).to_bytes(1, 'little'))
    sync_io.write((256).to_bytes(2, 'little'))
    sync_io.write(string.encode())
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await STRING.reader(data_base_reader)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, string)
    vampytest.assert_eq(data_base_reader.position, 259)


async def test__STRING__reader__end_of_file_reading_length():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 1),)):
        await STRING.reader(data_base_reader)


async def test__STRING__reader__end_of_file_reading_extended_length():
    """
    Tests whether ``STRING.reader`` works as intended.
    
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
        await STRING.reader(data_base_reader)


async def test__STRING__reader__end_of_file_reading_string():
    """
    Tests whether ``STRING.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading extended length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((5).to_bytes(1, 'little'))
    sync_io.write(b'aya')
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (1, 5),)):
        await STRING.reader(data_base_reader)


async def test__STRING__reader__extended_length_byte_count_out_of_range():
    """
    Tests whether ``STRING.reader`` works as intended.
    
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
        await STRING.reader(data_base_reader)


def test__STRING__producer__nulled():
    """
    Tests whether ``STRING.producer`` works as intended.
    
    Case: nulled.
    """
    string = None
    
    parts = [*STRING.producer(string)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(output, (0).to_bytes(1, 'little'))


def test__STRING__producer__regular_length():
    """
    Tests whether ``STRING.producer`` works as intended.
    
    Case: regular length.
    """
    string = 'ayaya'
    
    parts = [*STRING.producer(string)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (5).to_bytes(1, 'little'),
            string.encode(),
        ]),
    )


def test__STRING__producer__regular_length_unicode():
    """
    Tests whether ``STRING.producer`` works as intended.
    
    Case: regular length, unicode.
    """
    string = 'űűűűű'
    
    parts = [*STRING.producer(string)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (10).to_bytes(1, 'little'),
            string.encode(),
        ]),
    )


def test__STRING__producer__extended_length():
    """
    Tests whether ``STRING.producer`` works as intended.
    
    Case: extended length.
    """
    string = 'a' * 256
    
    parts = [*STRING.producer(string)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (64 | 2).to_bytes(1, 'little'),
            (256).to_bytes(2, 'little'),
            string.encode(),
        ]),
    )


def test__STRING__get_length__nulled():
    """
    Tests whether ``STRING.get_length`` works as intended.
    
    Case: nulled.
    """
    string = None
    
    output = STRING.get_length(string)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__STRING__get_length__regular_length():
    """
    Tests whether ``STRING.get_length`` works as intended.
    
    Case: regular length.
    """
    string = 'ayaya'
    
    output = STRING.get_length(string)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 6)


def test__STRING__get_length__regular_length_unicode():
    """
    Tests whether ``STRING.get_length`` works as intended.
    
    Case: regular length, unicode.
    """
    string = 'űűűűű'
    
    output = STRING.get_length(string)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 11)


def test__STRING__get_length__extended_length():
    """
    Tests whether ``STRING.get_length`` works as intended.
    
    Case: extended length.
    """
    string = 'a' * 256
    
    output = STRING.get_length(string)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 259)
