__all__ = ('HEADER',)

from ..data_base_reader import data_base_reader_read
from ..data_type import DataType
from ..data_type_ids import DATA_TYPE_ID_HEADER

# Structure
# byte 0 - 7: entry_count_allocated
#
# This field is used to determine how much entries to read.
#
# byte 8 - 15: entry_count_created

async def reader(data_base_reader):
    data = await data_base_reader_read(data_base_reader, 16)
    
    entry_count_allocated = int.from_bytes(data[0 : 8], 'little')
    entry_count_created = int.from_bytes(data[8 : 16], 'little')
    
    return (entry_count_allocated, entry_count_created)


def producer(header):
    entry_count_allocated, entry_count_created = header
    yield entry_count_allocated.to_bytes(8, 'little')
    yield entry_count_created.to_bytes(8, 'little')


def get_length(header):
    return 16


HEADER = DataType(
    DATA_TYPE_ID_HEADER,
    'header',
    tuple,
    False,
    False,
    reader,
    producer,
    get_length,
)
