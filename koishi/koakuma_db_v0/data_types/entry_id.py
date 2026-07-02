__all__ = ('ENTRY_ID',)

from ..data_base_reader import data_base_reader_read
from ..data_type import DataType
from ..data_type_ids import DATA_TYPE_ID_ENTRY_ID

# Structure
# byte 0 - 7: entry_id


async def reader(data_base_reader):
    data = await data_base_reader_read(data_base_reader, 8)
    return int.from_bytes(data, 'little')


def producer(entry_id):
    yield entry_id.to_bytes(8, 'little')


def get_length(entry_id):
    return 8


ENTRY_ID = DataType(
    DATA_TYPE_ID_ENTRY_ID,
    'entry id',
    int,
    False,
    False,
    reader,
    producer,
    get_length,
)
