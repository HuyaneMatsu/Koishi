from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import DATABASE_READING_ERROR_CODE_END_OF_FILE
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType

from ..entry_head import ENTRY_HEAD


def test__ENTRY_HEAD__structure():
    """
    Tests whether ``ENTRY_HEAD``'s structure is correct.
    """
    vampytest.assert_instance(ENTRY_HEAD, DataType)
    vampytest.assert_instance(ENTRY_HEAD.get_length, FunctionType)
    vampytest.assert_instance(ENTRY_HEAD.id, int)
    vampytest.assert_instance(ENTRY_HEAD.name, str)
    vampytest.assert_instance(ENTRY_HEAD.producer, FunctionType)
    vampytest.assert_instance(ENTRY_HEAD.reader, FunctionType)
    vampytest.assert_instance(ENTRY_HEAD.type_representation, type)
    vampytest.assert_instance(ENTRY_HEAD.type_representation_nullable, bool)
    vampytest.assert_instance(ENTRY_HEAD.type_representation_wrapped_into_list, bool)


async def test__ENTRY_HEAD__reader__good_space_empty():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, space, empty.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((128).to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (1, 0, 0))
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__ENTRY_HEAD__reader__good_empty():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, empty.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((0).to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (0, 0, 0))
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__ENTRY_HEAD__reader__good_space_regular_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, space, regular length.
    """
    entry_length = 5
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((128 | entry_length).to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (1, 0, entry_length))
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__ENTRY_HEAD__reader__good_space_regular_length__shifted_start():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, space, regular length; shifted start.
    """
    entry_length = 5
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(b'aa')
    sync_io.write((128 | entry_length).to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 2)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (1, 2, entry_length))
    vampytest.assert_eq(data_base_reader.position, 3)


async def test__ENTRY_HEAD__reader__good_regular_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, regular_length.
    """
    entry_length = 5
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write(entry_length.to_bytes(1, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (0, 0, entry_length))
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__ENTRY_HEAD__reader__good_space_extended_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, space, extended length.
    """
    entry_length = 256
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((128 | 64 | 2).to_bytes(1, 'little'))
    sync_io.write((entry_length).to_bytes(2, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (1, 0, entry_length))
    vampytest.assert_eq(data_base_reader.position, 3)


async def test__ENTRY_HEAD__reader__good_extended_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, extended_length.
    """
    entry_length = 256
    event_loop = get_event_loop()
    sync_io = BytesIO()
    sync_io.write((64 | 2).to_bytes(1, 'little'))
    sync_io.write(entry_length.to_bytes(2, 'little'))
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await ENTRY_HEAD.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, (0, 0, entry_length))
    vampytest.assert_eq(data_base_reader.position, 3)


async def test__ENTRY_HEAD__reader__end_of_file__read_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: End of file, reading length.
    """
    event_loop = get_event_loop()
    sync_io = BytesIO()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 1),)):
        await ENTRY_HEAD.reader(data_base_reader)


async def test__ENTRY_HEAD__reader__end_of_file__read_extended_length():
    """
    Tests whether ``ENTRY_HEAD.reader`` works as intended.
    
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
        await ENTRY_HEAD.reader(data_base_reader)


def test__ENTRY_HEAD__producer__space_empty():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: space, empty.
    """
    entry_head = (1, 0, 0)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        (128).to_bytes(1, 'little'),
    )


def test__ENTRY_HEAD__producer__empty():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: empty.
    """
    entry_head = (0, 0, 0)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        (0).to_bytes(1, 'little'),
    )


def test__ENTRY_HEAD__producer__space_regular_length():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: space, regular length.
    """
    entry_head = (1, 0, 10)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        (128 | 10).to_bytes(1, 'little'),
    )


def test__ENTRY_HEAD__producer__regular_length():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: regular length.
    """
    entry_head = (0, 0, 10)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        (10).to_bytes(1, 'little'),
    )


def test__ENTRY_HEAD__producer__space_extended_length():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: space, extended length.
    """
    entry_head = (1, 0, 256)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (128 | 64 | 2).to_bytes(1, 'little'),
            (256).to_bytes(2, 'little'),
        ]),
    )


def test__ENTRY_HEAD__producer__extended_length():
    """
    Tests whether ``ENTRY_HEAD.producer`` works as intended.
    
    Case: extended length.
    """
    entry_head = (0, 0, 256)
    
    parts = [*ENTRY_HEAD.producer(entry_head)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (64 | 2).to_bytes(1, 'little'),
            (256).to_bytes(2, 'little'),
        ]),
    )


def test__ENTRY_HEAD__get_length__space_empty():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: space, empty.
    """
    entry_head = (1, 0, 0)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__ENTRY_HEAD__get_length__empty():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: empty.
    """
    entry_head = (0, 0, 0)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__ENTRY_HEAD__get_length__space_regular_length():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: space, regular length.
    """
    entry_head = (1, 0, 10)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 11)


def test__ENTRY_HEAD__get_length__regular_length():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: regular length.
    """
    entry_head = (0, 0, 10)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 11)


def test__ENTRY_HEAD__get_length__space_extended_length():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: space, extended length.
    """
    entry_head = (1, 0, 256)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 259)


def test__ENTRY_HEAD__get_length__extended_length():
    """
    Tests whether ``ENTRY_HEAD.get_length`` works as intended.
    
    Case: extended length.
    """
    entry_head = (0, 0, 256)
    
    output = ENTRY_HEAD.get_length(entry_head)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 259)
