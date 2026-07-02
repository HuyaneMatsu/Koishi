from io import BytesIO
from types import FunctionType

import vampytest
from scarletio import get_event_loop

from ...constants import (
    DATABASE_READING_ERROR_CODE_END_OF_FILE, DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME, FIELD_FLAG_LISTING
)
from ...data_base_reader import DataBaseReader, data_base_reader_begin
from ...data_base_reading_error import DataBaseReadingError
from ...data_type import DataType
from ..string import STRING
from ..uint64 import UINT64
from ..fields_description import FIELDS_DESCRIPTION


def test__FIELDS_DESCRIPTION__structure():
    """
    Tests whether ``FIELDS_DESCRIPTION``'s structure is correct.
    """
    vampytest.assert_instance(FIELDS_DESCRIPTION, DataType)
    vampytest.assert_instance(FIELDS_DESCRIPTION.get_length, FunctionType)
    vampytest.assert_instance(FIELDS_DESCRIPTION.id, int)
    vampytest.assert_instance(FIELDS_DESCRIPTION.name, str)
    vampytest.assert_instance(FIELDS_DESCRIPTION.producer, FunctionType)
    vampytest.assert_instance(FIELDS_DESCRIPTION.reader, FunctionType)
    vampytest.assert_instance(FIELDS_DESCRIPTION.type_representation, type)
    vampytest.assert_instance(FIELDS_DESCRIPTION.type_representation_nullable, bool)
    vampytest.assert_instance(FIELDS_DESCRIPTION.type_representation_wrapped_into_list, bool)


async def test__FIELDS_DESCRIPTION__reader__good_empty():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, empty.
    """
    fields_description = ()
    sync_io = BytesIO()
    sync_io.write((0).to_bytes(1, 'little'))
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await FIELDS_DESCRIPTION.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, fields_description)
    vampytest.assert_eq(data_base_reader.position, 1)


async def test__FIELDS_DESCRIPTION__reader__good_two_fields():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, two fields.
    """
    fields_description = (
        (0, 'nyan', STRING.id, None),
        (0, 'rawr', UINT64.id, None),
    )
    sync_io = BytesIO()
    sync_io.write((2).to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'nyan')
    sync_io.write(STRING.id.to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'rawr')
    sync_io.write(UINT64.id.to_bytes(1, 'little'))
    
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await FIELDS_DESCRIPTION.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, fields_description)
    vampytest.assert_eq(data_base_reader.position, 15)


async def test__FIELDS_DESCRIPTION__reader__good_listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, listing.
    """
    fields_description = (
        (FIELD_FLAG_LISTING, 'nyan', STRING.id, None),
    )
    sync_io = BytesIO()
    sync_io.write((1).to_bytes(1, 'little'))
    
    sync_io.write((FIELD_FLAG_LISTING).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'nyan')
    sync_io.write(STRING.id.to_bytes(1, 'little'))
    
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await FIELDS_DESCRIPTION.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, fields_description)
    vampytest.assert_eq(data_base_reader.position, 8)


async def test__FIELDS_DESCRIPTION__reader__good_structure():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, structure.
    """
    fields_description = (
        (
            0,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    sync_io = BytesIO()
    sync_io.write((1).to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'nyan')
    sync_io.write((0).to_bytes(1, 'little'))
    
    sync_io.write((2).to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'name')
    sync_io.write(STRING.id.to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((5).to_bytes(1, 'little'))
    sync_io.write(b'value')
    sync_io.write(UINT64.id.to_bytes(1, 'little'))
    
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await FIELDS_DESCRIPTION.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, fields_description)
    vampytest.assert_eq(data_base_reader.position, 24)


async def test__FIELDS_DESCRIPTION__reader__good_structure_listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Good, structure listing.
    """
    fields_description = (
        (
            FIELD_FLAG_LISTING,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    sync_io = BytesIO()
    sync_io.write((1).to_bytes(1, 'little'))
    
    sync_io.write((FIELD_FLAG_LISTING).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'nyan')
    sync_io.write((0).to_bytes(1, 'little'))
    
    sync_io.write((2).to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((4).to_bytes(1, 'little'))
    sync_io.write(b'name')
    sync_io.write(STRING.id.to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((5).to_bytes(1, 'little'))
    sync_io.write(b'value')
    sync_io.write(UINT64.id.to_bytes(1, 'little'))
    
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    output = await FIELDS_DESCRIPTION.reader(data_base_reader)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, fields_description)
    vampytest.assert_eq(data_base_reader.position, 24)


async def test__FIELDS_DESCRIPTION__reader__bad_field_count():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Bad, field count.
    """
    sync_io = BytesIO()
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(DataBaseReadingError(DATABASE_READING_ERROR_CODE_END_OF_FILE, (0, 1))):
        await FIELDS_DESCRIPTION.reader(data_base_reader)


async def test__FIELDS_DESCRIPTION__reader__bad_empty_name():
    """
    Tests whether ``FIELDS_DESCRIPTION.reader`` works as intended.
    
    This function is a coroutine.
    
    Case: Bad, empty name.
    """
    sync_io = BytesIO()
    sync_io.write((1).to_bytes(1, 'little'))
    
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write((0).to_bytes(1, 'little'))
    sync_io.write(STRING.id.to_bytes(1, 'little'))
    
    event_loop = get_event_loop()
    
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, 0)
    
    with vampytest.assert_raises(
        DataBaseReadingError(DATABASE_READING_ERROR_CODE_FIELD_EMPTY_NAME, ())
    ):
        await FIELDS_DESCRIPTION.reader(data_base_reader)


def test__FIELDS_DESCRIPTION__producer__empty():
    """
    Tests whether ``FIELDS_DESCRIPTION.producer`` works as intended.
    
    Case: empty.
    """
    fields_description = ()
    
    parts = [*FIELDS_DESCRIPTION.producer(fields_description)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(output, (0).to_bytes(1, 'little'))


def test__FIELDS_DESCRIPTION__producer__two_fields():
    """
    Tests whether ``FIELDS_DESCRIPTION.producer`` works as intended.
    
    Case: two fields.
    """
    fields_description = (
        (0, 'nyan', STRING.id, None),
        (0, 'rawr', UINT64.id, None),
    )
    
    parts = [*FIELDS_DESCRIPTION.producer(fields_description)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (2).to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'nyan',
            STRING.id.to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'rawr',
            UINT64.id.to_bytes(1, 'little'),
        ])
    )


def test__FIELDS_DESCRIPTION__producer__listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.producer`` works as intended.
    
    Case: listing.
    """
    fields_description = (
        (FIELD_FLAG_LISTING, 'nyan', STRING.id, None),
    )
    
    parts = [*FIELDS_DESCRIPTION.producer(fields_description)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (1).to_bytes(1, 'little'),
            
            (FIELD_FLAG_LISTING).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'nyan',
            STRING.id.to_bytes(1, 'little'),
        ])
    )


def test__FIELDS_DESCRIPTION__producer__structure():
    """
    Tests whether ``FIELDS_DESCRIPTION.producer`` works as intended.
    
    Case: structure.
    """
    fields_description = (
        (
            0,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    
    parts = [*FIELDS_DESCRIPTION.producer(fields_description)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (1).to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'nyan',
            (0).to_bytes(1, 'little'),
            
            (2).to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'name',
            STRING.id.to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (5).to_bytes(1, 'little'),
            b'value',
            UINT64.id.to_bytes(1, 'little'),
        ])
    )


def test__FIELDS_DESCRIPTION__producer__structure_listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.producer`` works as intended.
    
    Case: structure listing.
    """
    fields_description = (
        (
            FIELD_FLAG_LISTING,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    
    parts = [*FIELDS_DESCRIPTION.producer(fields_description)]
    for part in parts:
        vampytest.assert_instance(part, bytes)
    
    output = b''.join(parts)
    vampytest.assert_eq(
        output,
        b''.join([
            (1).to_bytes(1, 'little'),
            
            (FIELD_FLAG_LISTING).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'nyan',
            (0).to_bytes(1, 'little'),
            
            (2).to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (4).to_bytes(1, 'little'),
            b'name',
            STRING.id.to_bytes(1, 'little'),
            
            (0).to_bytes(1, 'little'),
            (5).to_bytes(1, 'little'),
            b'value',
            UINT64.id.to_bytes(1, 'little'),
        ])
    )


def test__FIELDS_DESCRIPTION__get_length__empty():
    """
    Tests whether ``FIELDS_DESCRIPTION.get_length`` works as intended.
    
    Case: empty.
    """
    fields_description = ()
    
    output = FIELDS_DESCRIPTION.get_length(fields_description)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__FIELDS_DESCRIPTION__get_length__two_fields():
    """
    Tests whether ``FIELDS_DESCRIPTION.get_length`` works as intended.
    
    Case: two fields.
    """
    fields_description = (
        (0, 'nyan', STRING.id, None),
        (0, 'rawr', UINT64.id, None),
    )
    
    output = FIELDS_DESCRIPTION.get_length(fields_description)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 15)


def test__FIELDS_DESCRIPTION__get_length__listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.get_length`` works as intended.
    
    Case: listing.
    """
    fields_description = (
        (FIELD_FLAG_LISTING, 'nyan', STRING.id, None),
    )
    
    output = FIELDS_DESCRIPTION.get_length(fields_description)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 8)


def test__FIELDS_DESCRIPTION__get_length__structure():
    """
    Tests whether ``FIELDS_DESCRIPTION.get_length`` works as intended.
    
    Case: structure.
    """
    fields_description = (
        (
            0,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    
    output = FIELDS_DESCRIPTION.get_length(fields_description)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 24)


def test__FIELDS_DESCRIPTION__get_length__structure_listing():
    """
    Tests whether ``FIELDS_DESCRIPTION.get_length`` works as intended.
    
    Case: structure listing.
    """
    fields_description = (
        (
            FIELD_FLAG_LISTING,
            'nyan',
            0,
            (
                (0, 'name', STRING.id, None),
                (0, 'value', UINT64.id, None),
            ),
        ),
    )
    
    output = FIELDS_DESCRIPTION.get_length(fields_description)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 24)
