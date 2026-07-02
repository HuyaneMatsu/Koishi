__all__ = ('UINT64',)

from ..data_base_reader import data_base_reader_read
from ..data_type import DataType
from ..data_type_ids import UINT64

# Structure
# byte 0 - 7: uint64


async def reader(data_base_reader):
    data = await data_base_reader_read(data_base_reader, 8)
    return int.from_bytes(data, 'little')


def producer(uint64):
    yield uint64.to_bytes(8, 'little')


def get_length(uint64):
    return 8


UINT64 = DataType(
    UINT64,
    'unsigned integer 64',
    int,
    False,
    False,
    reader,
    producer,
    get_length,
)
