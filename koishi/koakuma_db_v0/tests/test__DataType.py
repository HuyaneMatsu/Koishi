from types import FunctionType

import vampytest

from ..data_type import DataType


def _assert_fields_set(data_type):
    """
    Asserts whether every attributes are set of the given data type.
    
    Parameters
    ----------
    data_type :: ``DtaType``
    """
    vampytest.assert_instance(data_type, DataType)
    vampytest.assert_instance(data_type.get_length, FunctionType)
    vampytest.assert_instance(data_type.id, int)
    vampytest.assert_instance(data_type.name, str)
    vampytest.assert_instance(data_type.producer, FunctionType)
    vampytest.assert_instance(data_type.reader, FunctionType)
    vampytest.assert_instance(data_type.type_representation, type)
    vampytest.assert_instance(data_type.type_representation_nullable, bool)
    vampytest.assert_instance(data_type.type_representation_wrapped_into_list, bool)


def test__DataType__new():
    """
    Tests whether ``DataType.__new__`` work as intended.
    """
    data_type_id = 100
    name = 'shrimp'
    type_representation = str
    type_representation_nullable = True
    type_representation_wrapped_into_list = False
    
    async def reader(data_reader):
        await data_reader.read(1)
        return 'a'
    
    def producer(value):
        yield b'a'
    
    def get_length(value):
        return 1
    
    data_type = DataType(
        data_type_id,
        name,
        type_representation,
        type_representation_nullable,
        type_representation_wrapped_into_list,
        reader,
        producer,
        get_length,
    )
    _assert_fields_set(data_type)
    
    vampytest.assert_is(data_type.get_length, get_length)
    vampytest.assert_eq(data_type.id, data_type_id)
    vampytest.assert_eq(data_type.name, name)
    vampytest.assert_is(data_type.producer, producer)
    vampytest.assert_is(data_type.reader, reader)
    vampytest.assert_is(data_type.type_representation, type_representation)
    vampytest.assert_eq(data_type.type_representation_nullable, type_representation_nullable)
    vampytest.assert_eq(data_type.type_representation_wrapped_into_list, type_representation_wrapped_into_list)


def test__DataType__repr():
    """
    Tests whether ``DataType.__repr__`` works as intended.
    """
    data_type_id = 100
    name = 'shrimp'
    type_representation = str
    type_representation_nullable = True
    type_representation_wrapped_into_list = False
    
    async def reader(data_reader):
        await data_reader.read(1)
        return 'a'
    
    def producer(value):
        yield b'a'
    
    def get_length(value):
        return 1
    
    data_type = DataType(
        data_type_id,
        name,
        type_representation,
        type_representation_nullable,
        type_representation_wrapped_into_list,
        reader,
        producer,
        get_length,
    )
    
    output = repr(data_type)
    vampytest.assert_instance(output, str)
