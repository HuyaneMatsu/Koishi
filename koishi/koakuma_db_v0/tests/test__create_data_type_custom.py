from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ..custom_data_types import create_data_type_custom
from ..data_base_reader import DataBaseReader, data_base_reader_begin
from ..data_type import DataType

from .helpers import TestStructure


def test__create_data_type_custom__structure():
    """
    Tests whether ``create_data_type_custom`` returns an object with the correct structure.
    """
    data_type = create_data_type_custom(TestStructure)
    
    vampytest.assert_instance(data_type, DataType)
    
    vampytest.assert_instance(data_type.get_length, FunctionType)
    vampytest.assert_instance(data_type.id, int)
    vampytest.assert_instance(data_type.name, str)
    vampytest.assert_instance(data_type.producer, FunctionType)
    vampytest.assert_instance(data_type.reader, FunctionType)
    vampytest.assert_instance(data_type.type_representation, type)
    vampytest.assert_instance(data_type.type_representation_nullable, bool)
    vampytest.assert_instance(data_type.type_representation_wrapped_into_list, bool)
    
    vampytest.assert_eq(data_type.id, 0)
    vampytest.assert_eq(data_type.name, TestStructure.__name__)
    vampytest.assert_is(data_type.type_representation, TestStructure)
    vampytest.assert_eq(data_type.type_representation_nullable, False)
    vampytest.assert_eq(data_type.type_representation_wrapped_into_list, False)


async def test__create_data_type_custom__reader():
    """
    Tests whether ``create_data_type_custom`` returns a data type with correct reader.
    
    This function is a coroutine.
    """
    data_type = create_data_type_custom(TestStructure)
    
    name = 'nyan'
    value = 123333
    
    sync_io = BytesIO()
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(name.encode())
    sync_io.write(value.to_bytes(8, 'little'))
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await data_type.reader(data_base_reader)
    
    vampytest.assert_instance(output, TestStructure)
    vampytest.assert_instance(output.name, str, nullable = True)
    vampytest.assert_instance(output.value, int)
    vampytest.assert_eq(output.name, name)
    vampytest.assert_eq(output.value, value)
    
    vampytest.assert_eq(data_base_reader.position, 13)


def test__create_data_type_custom__producer():
    """
    Tests whether ``create_data_type_custom`` returns a data type with correct producer.
    """
    data_type = create_data_type_custom(TestStructure)
    
    name = 'nyan'
    value = 123333
    
    structure = TestStructure((name, value),)
    
    parts = [*data_type.producer(structure)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    
    vampytest.assert_eq(
        output,
        b''.join([
            (4).to_bytes(1, 'little'),
            name.encode(),
            (value).to_bytes(8, 'little'),
        ]),
    )


def test__create_data_type_custom__get_length():
    """
    Tests whether ``create_data_type_custom`` returns a data type with correct get_length.
    """
    data_type = create_data_type_custom(TestStructure)
    
    name = 'nyan'
    value = 123333
    
    structure = TestStructure((name, value),)
    
    output = data_type.get_length(structure)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 13)
