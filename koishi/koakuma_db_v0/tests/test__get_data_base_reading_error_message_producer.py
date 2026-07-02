import vampytest

from ..constants import (
    DATABASE_READING_ERROR_CODE_END_OF_FILE, DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE,
    DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH, DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME,
    DATABASE_READING_ERROR_CODE_UNKNOWN_DATA_TYPE_ID
)
from ..data_base_reading_error import DataBaseReadingError, get_data_base_reading_error_message_producer
from ..data_types import STRING, UINT64


def _iter_options():
    yield (
        0,
        (),
        None,
    )
    
    yield (
        DATABASE_READING_ERROR_CODE_END_OF_FILE,
        (
            20,
            10,
        ),
        'Reached end of file at position 20, while still expecting to read 10 more bytes.',
    )
    
    yield (
        DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE,
        (
            20,
            STRING,
            10,
        ),
        (
            'Could not read string. Its length was supposedly stored on over 8 bytes; '
            'extended_length_byte_count = 10; position_after_reading = 20.'
        ),
    )
    
    yield (
        DATABASE_READING_ERROR_CODE_UNKNOWN_DATA_TYPE_ID,
        (
            255,
        ),
        'Unknown data type while reading data base header; data_type_id = 255.'
    )
    
    yield (
        DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME,
        (),
        'A field in data base has empty name.'
    )
    
    fields_0 = (
        (0, 'nyan', STRING.id, None),
    )
    
    fields_1 = (
        (0, 'rawr', UINT64.id, None),
    )
    
    yield (
        DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH,
        (
            fields_0,
            fields_1,
        ),
        f'Database fields and the fields read mismatch; expected_fields = {fields_0!r}; read_fields = {fields_1!r}.'
    )
    
    yield (
        1000,
        (),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_data_base_reading_error_message_producer(error_code, metadata):
    """
    Parameters
    ----------
    error_code : `int`
        Error code to get exception producer for.
    
    metadata : `int`
        Exception metadata.
    
    Returns
    -------
    output : `None | str`
    """
    producer = get_data_base_reading_error_message_producer(error_code)
    if producer is None:
        return None
    
    exception = DataBaseReadingError(error_code, metadata)
    parts = [*producer(exception)]
    
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
