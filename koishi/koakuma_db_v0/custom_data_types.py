__all__ = ('create_data_type_custom', 'create_data_type_listing')

from .data_type import DataType
from .helpers import convert_length_to_extended_length_byte_count, produce_length_bytes, read_length
from .structure import Structure


def create_data_type_custom(structure):
    """
    Creates a custom data type.
    
    Parameters
    ----------
    structure : ``Structure``
        Structure to create data type for.
    
    Returns
    -------
    data_type : ``DataType``
    """
    assert isinstance(structure, Structure)
    
    fields = structure.__fields__
    readers = (*(field.data_type.reader for field in fields),)
    producers = (*(field.data_type.producer for field in fields),)
    get_lengths = (*(field.data_type.get_length for field in fields),)
    
    
    async def reader(data_base_reader):
        nonlocal readers, structure
        
        read = []
        for reader in readers:
            read.append(await reader(data_base_reader))
        
        return structure(read)
    
    
    def producer(value):
        nonlocal producers
        for producer, element in zip(producers, value):
            yield from producer(element)
    
    
    def get_length(value):
        nonlocal get_lengths
        length = 0
        for get_length, element in zip(get_lengths, value):
            length += get_length(element)
        return length
    
    
    return DataType(
        0,
        structure.__name__,
        structure,
        False,
        False,
        reader,
        producer,
        get_length,
    )


def create_data_type_listing(data_type):
    """
    Creates a custom data type.
    
    Parameters
    ----------
    data_type : ``DataType``
        Data type to created listing for.
    
    Returns
    -------
    data_type_listing : ``DataType``
    """
    assert type(data_type) is DataType
    assert not data_type.type_representation_wrapped_into_list
    
    data_type_reader = data_type.reader
    data_type_producer = data_type.producer
    data_type_get_length = data_type.get_length
    
    
    async def reader(data_base_reader):
        nonlocal data_type_listing, data_type_reader
        length = await read_length(data_base_reader, data_type_listing)
        if not length:
            return None
        
        read = []
        for index in range(length):
            read.append(await data_type_reader(data_base_reader))
        
        return tuple(read)
    
    
    def producer(value):
        nonlocal data_type_producer
        if value is None:
            yield b'\000'
        else:
            yield from produce_length_bytes(len(value))
            for element in value:
                yield from data_type_producer(element)
    
    
    def get_length(value):
        nonlocal data_type_get_length
        length = 1
        if (value is not None):
            if length > 63:
                length += convert_length_to_extended_length_byte_count(len(value))
            
            for element in value:
                length += data_type_get_length(element)
        
        return length
    
    
    data_type_listing = DataType(
        data_type.id,
        f'{data_type.name!s} listing',
        data_type.type_representation,
        True,
        True,
        reader,
        producer,
        get_length,
    )
    return data_type_listing
