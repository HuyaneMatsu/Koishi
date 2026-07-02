__all__ = ('FIELDS_DESCRIPTION',)

from ..constants import DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME
from ..data_base_reader import data_base_reader_read
from ..data_base_reading_error import DataBaseReadingError
from ..data_type import DataType
from ..data_type_ids import DATA_TYPE_ID_FIELDS_DESCRIPTION
from ..helpers import get_length_encoded_byte_count, produce_length_bytes, read_length

from .string import get_length as string_get_length, producer as string_producer, reader as string_reader


# Structure
# bit
# | 7        | 6               | 5 | 4 | 3 | 2 | 1 | 0 |
# | reserved | extended length | length                |
#
# If extended length is defined, then `length` cannot be greater than 8. The reader will issue a length times repeated
# structure reading.
#
# Structure reading consists of the following reads:
# - read flags (1 byte)
# - read name (string read; cannot be empty)
# - read data_type_id (1 byte; results in 0 when reading a structure)
# - read sub fields (skip if not reading a structure)


async def reader(data_base_reader):
    fields = []
    
    length = await read_length(data_base_reader, FIELDS_DESCRIPTION)
    for _ in range(length):
        data = await data_base_reader_read(data_base_reader, 1)
        flags = data[0]
        

        name = await string_reader(data_base_reader)
        if (name is None):
            raise DataBaseReadingError(
                DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME,
                (),
            )
        
        data = await data_base_reader_read(data_base_reader, 1)
        data_type_id = data[0]
        
        if data_type_id:
            sub_description = None
        else:
            sub_description = await reader(data_base_reader)
        
        fields.append((flags, name, data_type_id, sub_description))
    
    return tuple(fields)


def producer(fields_description):
    yield from produce_length_bytes(len(fields_description))
    for flags, name, data_type_id, sub_description in fields_description:
        yield flags.to_bytes(1, 'little')
        yield from string_producer(name)
        yield data_type_id.to_bytes(1, 'little')
        if (sub_description is not None):
            yield from producer(sub_description)


def get_length(fields_description):
    cumulative_length = get_length_encoded_byte_count(len(fields_description))
    for flags, name, data_type_id, sub_description in fields_description:
        cumulative_length += 2 + string_get_length(name)
        if (sub_description is not None):
            cumulative_length += get_length(sub_description)
    
    return cumulative_length


FIELDS_DESCRIPTION = DataType(
    DATA_TYPE_ID_FIELDS_DESCRIPTION,
    'fields description',
    str,
    True,
    False,
    reader,
    producer,
    get_length,
)
