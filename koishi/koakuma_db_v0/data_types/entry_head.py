__all__ = ('ENTRY_HEAD',)

from ..constants import DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE
from ..data_base_reader import data_base_reader_read
from ..data_base_reading_error import DataBaseReadingError
from ..data_type import DataType
from ..data_type_ids import DATA_TYPE_ID_ENTRY_HEAD
from ..helpers import convert_length_to_extended_length_byte_count, get_length_encoded_byte_count


# Structure
# byte 16 : length
# | 7      | 6               |  5    |    4 |    3 |    2  |    1 |    0  |
# | space | extended length |             length                         |
#
# ? byte 17 - length + length & 63
# The extended size of the field.


async def reader(data_base_reader):
    start_position = data_base_reader.position
    data = await data_base_reader_read(data_base_reader, 1)
    length = data[0]
    if not length:
        return (0, start_position, 0)
    
    space = length >> 7
    extended_length = length & 64
    length &= 63
    
    if not extended_length:
        entry_length = length
    else:
        if length > 8:
            raise DataBaseReadingError(
                DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE,
                (data_base_reader.position, ENTRY_HEAD, length),
            )
        
        data = await data_base_reader_read(data_base_reader, length)
        entry_length = int.from_bytes(data, 'little')
    
    return space, start_position, entry_length


def producer(entry_head):
    space, starting_position, entry_length = entry_head
    
    if entry_length < 64:
        yield ((space << 7) | entry_length).to_bytes(1, 'little')
    else:
        length_extension_length = convert_length_to_extended_length_byte_count(entry_length)
        yield ((space << 7) | 64 | length_extension_length).to_bytes(1, 'little')
        yield entry_length.to_bytes(length_extension_length, 'little')


def get_length(entry_head):
    entry_length = entry_head[2]
    return entry_length + get_length_encoded_byte_count(entry_length)


ENTRY_HEAD = DataType(
    DATA_TYPE_ID_ENTRY_HEAD,
    'entry head',
    tuple,
    True,
    False,
    reader,
    producer,
    get_length,
)
