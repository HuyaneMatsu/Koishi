__all__ = ('STRING',)

from ..data_base_reader import data_base_reader_read
from ..data_type import DataType
from ..data_type_ids import DATA_TYPE_ID_STRING
from ..helpers import (
    get_length_encoded_byte_count, get_string_encoded_length, produce_length_bytes, read_length
)

# Structure
# bit
# | 7        | 6               | 5 | 4 | 3 | 2 | 1 | 0 |
# | reserved | extended length | length                |
#
# If extended length is defined, then `length` cannot be greater than 8. The reader will issue a `length` length
# read to read the string's actual length.


async def reader(data_base_reader):
    length = await read_length(data_base_reader, STRING)
    if not length:
        return None
    
    data = await data_base_reader_read(data_base_reader, length)
    
    # Cannot decode memoryview; If it is memoryview, we can convert it to `bytes` tho.
    # If it is already `bytes`, will just return itself.
    return bytes(data).decode()


def producer(string):
    if string is None:
        yield b'\000'
    else:
        data = string.encode()
        yield from produce_length_bytes(len(data))
        yield data


def get_length(string):
    length = get_string_encoded_length(string)
    return get_length_encoded_byte_count(length) + length


STRING = DataType(
    DATA_TYPE_ID_STRING,
    'string',
    str,
    True,
    False,
    reader,
    producer,
    get_length,
)
