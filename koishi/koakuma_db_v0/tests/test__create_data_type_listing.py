from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ..custom_data_types import create_data_type_listing
from ..data_base_reader import DataBaseReader, data_base_reader_begin
from ..data_type import DataType
from ..data_types import STRING


def test__create_data_type_listing__structure():
    """
    Tests whether ``create_data_type_listing`` returns an object with the correct structure.
    """
    data_type = create_data_type_listing(STRING)
    
    vampytest.assert_instance(data_type, DataType)
    
    vampytest.assert_instance(data_type.get_length, FunctionType)
    vampytest.assert_instance(data_type.id, int)
    vampytest.assert_instance(data_type.name, str)
    vampytest.assert_instance(data_type.producer, FunctionType)
    vampytest.assert_instance(data_type.reader, FunctionType)
    vampytest.assert_instance(data_type.type_representation, type)
    vampytest.assert_instance(data_type.type_representation_nullable, bool)
    vampytest.assert_instance(data_type.type_representation_wrapped_into_list, bool)
    
    vampytest.assert_eq(data_type.id, STRING.id)
    vampytest.assert_has(data_type.name, STRING.name)
    vampytest.assert_is(data_type.type_representation, STRING.type_representation)
    vampytest.assert_eq(data_type.type_representation_nullable, True)
    vampytest.assert_eq(data_type.type_representation_wrapped_into_list, True)


async def test__create_data_type_listing__reader__empty():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct reader.
    
    This function is a coroutine.
    
    Case: empty.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = None
    
    sync_io = BytesIO()
    sync_io.write(b'\000')
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await data_type.reader(data_base_reader)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_eq(output, listing)
    
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__create_data_type_listing__reader__regular_length():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct reader.
    
    This function is a coroutine.
    
    Case: regular length.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = (
        'nyan',
        'rawr',
        'pyon',
    )
    
    sync_io = BytesIO()
    sync_io.write((3).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(listing[0].encode())
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(listing[1].encode())
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(listing[2].encode())
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await data_type.reader(data_base_reader)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_eq(output, listing)
    
    vampytest.assert_eq(data_base_reader.position, 16)


def test__create_data_type_listing__producer__empty():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct producer.
    
    Case: empty.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = None
    
    parts = [*data_type.producer(listing)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    
    vampytest.assert_eq(
        output,
        b'\000',
    )


def test__create_data_type_listing__producer__regular_length():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct producer.
    
    Case: regular length.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = (
        'nyan',
        'rawr',
        'pyon',
    )
    
    parts = [*data_type.producer(listing)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    
    vampytest.assert_eq(
        output,
        b''.join([
            (3).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            listing[0].encode(),
            (4).to_bytes(1, 'little'),
            listing[1].encode(),
            (4).to_bytes(1, 'little'),
            listing[2].encode(),
        ]),
    )


def test__create_data_type_listing__get_length__empty():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct get_length.
    
    Case: empty.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = None
    
    output = data_type.get_length(listing)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__create_data_type_listing__get_length__regular_length():
    """
    Tests whether ``create_data_type_listing`` returns a data type with correct get_length.
    
    Case: regular length.
    """
    data_type = create_data_type_listing(STRING)
    
    listing = (
        'nyan',
        'rawr',
        'pyon',
    )
    
    output = data_type.get_length(listing)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 16)
