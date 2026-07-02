__all__ = (
    'data_base_create', 'data_base_connect', 'data_base_connected_entry_create', 'data_base_connected_entry_delete',
    'data_base_connected_entry_modify', 'data_base_connected_save',
)

from functools import partial as partial_function
from os.path import abspath as get_absolute_path

from scarletio import RichAttributeErrorBaseType
from scarletio import get_event_loop

from .constants import DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH
from .data_base_reader import DataBaseReader, data_base_reader_begin, data_base_reader_skip
from .data_base_reading_error import DataBaseReadingError
from .data_types import ENTRY_HEAD, FIELDS_DESCRIPTION, HEADER
from .helpers import build_length_bytes, build_space_bytes
from .structure import get_fields_description


def _open_sync(file_path):
    """
    Opens the file for reading and writing.
    
    Parameters
    ----------
    file_path : `str`
        Path to the file.
    
    Returns
    -------
    sync_io : `_io._IOBase`
    """
    return open(file_path, 'rb+')


async def data_base_connect(file_path, entry_type, position):
    """
    Connects the data base to the given path.
    
    This function is a coroutine.
    
    Parameters
    ----------
    file_path : `str`
        Path to the file.
    
    entry_type : ``instance<instance<EntryStructure>>``
        Data base entry type to match and read into.
    
    position : `int`
        Position to start reading at.
    
    Returns
    -------
    data_base_connected : ``DataBaseConnected``
    
    Raises
    ------
    DataBaseReadingError
    """
    file_path = get_absolute_path(file_path)
    event_loop = get_event_loop()
    sync_io = await event_loop.run_in_executor(partial_function(_open_sync, file_path))
    entry_count_allocated, entry_count_created, entries, spaces, end_position = await _data_base_read(
        event_loop, entry_type, sync_io, position
    )
    return DataBaseConnected(
        file_path,
        entry_type,
        event_loop,
        sync_io,
        position,
        end_position,
        entry_count_allocated,
        entry_count_created,
        entries,
        spaces,
    )


def _open_and_write_initial_data_sync(file_path, position, initial_data):
    """
    Writes initial data to the data base.
    
    Parameters
    ----------
    file_path : `str`
        Path to the file.
    
    position : `int`
        Position to start writing at.
    
    initial_data : `bytes`
        Data to write initially.
    
    Returns
    -------
    sync_io : `_io._IOBase`
    """
    sync_io = open(file_path, 'wb+')
    sync_io.seek(position)
    sync_io.write(initial_data)
    sync_io.flush()
    return sync_io


async def data_base_create(file_path, entry_type, position):
    """
    Creates a new data base.
    
    This function is a coroutine.
    
    file_path : `str`
        Path to the file.
    
    entry_type : ``instance<instance<EntryStructure>>``
        Data base entry type to match and read into.
    
    position : `int`
        Position to start reading at.
    
    """
    file_path = get_absolute_path(file_path)
    event_loop = get_event_loop()
    initial_data = b''.join([
        b'\000' * 16,
        *FIELDS_DESCRIPTION.producer(get_fields_description(entry_type.__fields__)),
    ])
    sync_io = await event_loop.run_in_executor(
        partial_function(_open_and_write_initial_data_sync, file_path, position, initial_data)
    )
    
    return DataBaseConnected(
        file_path,
        entry_type,
        event_loop,
        sync_io,
        position,
        position + len(initial_data),
        0,
        0,
        {},
        {},
    )


async def _data_base_read(event_loop, entry_type, sync_io, position):
    """
    Reads the data base.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_loop : ``EventThread``
        The event loop to use.
    
    entry_type : ``instance<instance<EntryStructure>>``
        Data base entry type to match and read into.
    
    sync_io : `_io._IOBase`
        Io to use.
    
    position : `int`
        Position to start reading at.
    
    Returns
    -------
    entry_count_allocated_and_entry_count_created_and_entries_and_spaces_and_end_position : ``(int, int, dict<int, entry_type>, dict<int, list<int>>, int)``
    
    Raises
    ------
    DataBaseReadingError
    """
    data_base_reader = DataBaseReader(event_loop, sync_io)
    data_base_reader_begin(data_base_reader, position)
    
    entry_count_allocated, entry_count_created = await HEADER.reader(data_base_reader)
    
    fields_description_received = await FIELDS_DESCRIPTION.reader(data_base_reader)
    fields_description_expected = get_fields_description(entry_type.__fields__)
    if fields_description_received != fields_description_expected:
        raise DataBaseReadingError(
            DATABASE_READING_ERROR_CODE_FIELDS_DESCRIPTION_MISMATCH,
            (fields_description_received, fields_description_expected),
        )
    
    readers = (*(field.data_type.reader for field in entry_type.__fields__),)
    
    entries = {}
    spaces = {}
    
    for _ in range(entry_count_allocated):
        space, starting_position, entry_length = await ENTRY_HEAD.reader(data_base_reader)
        if space:
            await data_base_reader_skip(data_base_reader, entry_length)
            
            try:
                spaces_for_length = spaces[entry_length]
            except KeyError:
                spaces[entry_length] = spaces_for_length = []
            spaces_for_length.append(starting_position)
            continue
        
        entry_values = [starting_position, entry_length]
        for reader in readers:
            field_value = await reader(data_base_reader)
            entry_values.append(field_value)
        
        entries[entry_values[2]] = entry_type(entry_values)
        continue
    
    return entry_count_allocated, entry_count_created, entries, spaces, data_base_reader.position


def _make_serialised_entry_parts(entry_type, entry_values):
    """
    Makes serialised entry parts. The returned list's first element is empty, able to be replaced.
    
    Parameters
    ----------
    entry_type : ``instance<instance<EntryStructure>>``
        Data base entry type to match and read into.
    
    entry_values : `list<*(int, int, int), *iterable<object>>`
        Entry values.
    
    Returns
    -------
    parts : `list<bytes>`
    """
    serialised_entry_parts = [b'']
    
    index = 2
    for field in entry_type.__fields__:
        serialised_entry_parts.extend(field.data_type.producer(entry_values[index]))
        index += 1
    
    return serialised_entry_parts


def _write_write_queue_sync(sync_io, write_queue):
    """
    Writes write queue sync.
    
    sync_io : `_io._IOBase`
        Io to use.
    
    write_queue : `list<(int, bytes)>`
        Location - data pairs.
    """
    for start_position, data in write_queue:
        sync_io.seek(start_position)
        sync_io.write(data)
    
    sync_io.flush()


def _mark_as_space(data_base_connected, start_position, entry_length):
    """
    Marks the location of length as space.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    
    start_position : `int`
        The position where the space starts.
    
    entry_length : `int`
        Entry length that can fit in size.
    """
    length_bytes = build_space_bytes(entry_length)
    
    spaces = data_base_connected.spaces
    try:
        spaces_for_length = spaces[entry_length]
    except KeyError:
        spaces[entry_length] = spaces_for_length = []
    
    spaces_for_length.append(start_position)
    
    if start_position >= data_base_connected.end_position_real:
        length_bytes += b'\000' * entry_length
    
    _insert_to_write_queue(data_base_connected, start_position, length_bytes)


def _find_insertion_fit(data_base_connected, header_length, entry_length):
    """
    Finds a place in the data base to fit an entry of the given size.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    
    header_length : `int`
        The entry's header's size.
    
    entry_length : `int`
        Entry length that can fit in size.
    """
    spaces = data_base_connected.spaces
    try:
        spaces_for_length = spaces[entry_length]
    except KeyError:
        start_position = data_base_connected.end_position
        data_base_connected.end_position = start_position + header_length + entry_length
        data_base_connected.entry_count_allocated += 1
    else:
        start_position = spaces_for_length.pop()
        if not spaces_for_length:
            del spaces[entry_length]
    
    return start_position


def _insert_to_write_queue(data_base_connected, start_position, data):
    """
    Inserts a write action to the write queue.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    
    start_position : `int`
        Position to start writing at.
    
    data : `bytes`
        Data to write.
    """
    write_queue = data_base_connected.write_queue
    if (write_queue is None):
        data_base_connected.write_queue = write_queue = []
    
    item = (start_position, data)
    for index in range(len(write_queue)):
        if write_queue[index][0] == start_position:
            write_queue[index] = item
            break
    else:
        write_queue.append(item)


def data_base_connected_entry_create(data_base_connected, **keyword_parameters):
    """
    Crates a data base entry.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    
    **keyword_parameters : KeyWord parameters
        Keyword parameters to create the entry with.
    
    Returns
    -------
    entry : `data_base_connected.entry_type`
    """
    entry_id = data_base_connected.entry_count_created + 1
    
    entry_type = data_base_connected.entry_type
    entry_values = [0, 0, entry_id]
    
    fields = entry_type.__fields__
    for index in range(1, len(fields)):
        field = fields[index]
        try:
            value = keyword_parameters[field.name]
        except KeyError as exception:
            raise RuntimeError(f'f{field.name} is required, but not present.') from exception
        
        if __debug__:
            data_type = field.data_type
            type_representation = data_type.type_representation
            type_representation_nullable = data_type.type_representation_nullable
            type_representation_wrapped_into_list = data_type.type_representation_wrapped_into_list
            
            if type_representation_wrapped_into_list:
                if (value is not None):
                    assert (type(value) is tuple)
                    for element in value:
                        assert (type(element) is type_representation)
            else:
                if type_representation_nullable:
                    assert (value is None) or (type(value) is type_representation)
                else:
                    assert (type(value) is type_representation)
        
        entry_values.append(value)
    
    data_base_connected.entry_count_created = entry_id
    
    serialised_entry_parts = _make_serialised_entry_parts(entry_type, entry_values)
    
    entry_length = sum(len(part) for part in serialised_entry_parts)
    
    length_bytes = build_length_bytes(entry_length)
    serialised_entry_parts[0] = length_bytes
    
    header_length = len(length_bytes)
    serialised_entry = b''.join(serialised_entry_parts)
    serialised_entry_parts = None
    start_position = _find_insertion_fit(data_base_connected, header_length, entry_length)
    
    entry_values[0] = start_position
    entry_values[1] = entry_length
    _insert_to_write_queue(data_base_connected, start_position, serialised_entry)
    entry = entry_type(entry_values)
    data_base_connected.entries[entry_id] = entry
    return entry


def data_base_connected_entry_modify(data_base_connected, entry, **keyword_parameters):
    """
    Modified a data base entry.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    
    entry : `data_base_connected.entry_type`
        The entry to modify.
    
    **keyword_parameters : KeyWord parameters
        Keyword parameters to modify the entry with.
    
    Returns
    -------
    entry : `data_base_connected.entry_type`
    """
    entry_type = data_base_connected.entry_type
    start_position_old = entry[0]
    entry_length_old = entry[1]
    entry_id = entry[2]
    entry_values = [start_position_old, entry_length_old, entry_id]
    length_difference = 0
    
    fields = entry_type.__fields__
    for index in range(1, len(fields)):
        field = fields[index]
        data_type = field.data_type
        old_value = entry[index + 2]
        try:
            new_value = keyword_parameters[field.name]
        except KeyError:
            new_value = old_value
        
        else:
            get_length = data_type.get_length
            length_difference += get_length(new_value) - get_length(old_value)
            
            assert type(new_value) is field.data_type.type_representation
        
        entry_values.append(new_value)
    
    
    if length_difference == 0:
        start_position_new = start_position_old
        entry_length_new = entry_length_old
    else:
        _mark_as_space(data_base_connected, start_position_old, entry_length_old)
        entry_length_new = entry[1] + length_difference
        length_bytes = build_length_bytes(entry_length_new)
        header_length = len(length_bytes)
        start_position_new = _find_insertion_fit(data_base_connected, header_length, entry_length_new)
        
        entry_values[0] = start_position_new
        entry_values[1] = entry_length_new
    
    serialised_entry_parts = _make_serialised_entry_parts(entry_type, entry_values)
    serialised_entry_parts[0] = build_length_bytes(entry_length_new)
    serialised_entry = b''.join(serialised_entry_parts)
    serialised_entry_parts = None
    _insert_to_write_queue(data_base_connected, start_position_new, serialised_entry)
    entry = entry_type(entry_values)
    data_base_connected.entries[entry_id] = entry
    return entry


def data_base_connected_entry_delete(data_base_connected, entry):
    """
    Modified a data base entry.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        The connected data base.
    """
    try:
        del data_base_connected.entries[entry[2]]
    except KeyError:
        pass
    else:
        _mark_as_space(data_base_connected, entry[0], entry[1])


async def data_base_connected_save(data_base_connected):
    """
    Saves the write queue of the connected data base.
    
    This function is a coroutine.
    
    Parameters
    ----------
    data_base_connected : ``DataBaseConnected``
        Connected data base to work with.
    """
    write_queue = data_base_connected.write_queue
    if (write_queue is None):
        return
    
    write_queue.append((
        data_base_connected.start_position,
        (
            data_base_connected.entry_count_allocated.to_bytes(8, 'little') +
            data_base_connected.entry_count_created.to_bytes(8, 'little')
        ),
    ))
    data_base_connected.write_queue = None
    data_base_connected.end_position_real = data_base_connected.end_position
    await data_base_connected.event_loop.run_in_executor(
        partial_function(_write_write_queue_sync, data_base_connected.sync_io, write_queue)
    )


class DataBaseConnected(RichAttributeErrorBaseType):
    """
    A connected data base.
    
    Attributes
    ----------
    end_position : `int`
        Where the data base ends in the file.
    
    end_position_real : `int`
        Where the file currently ends.
    
    entries : `dict<int, .entry_type>`
        The entries of the data base.
    
    entry_count_allocated : `int`
        How much entries are allocated.
    
    entry_count_created : `int`
        How much entries were created.
    
    entry_type : ``EntryStructure``
        The held entries' type.
    
    event_loop : ``EventThread``
        Event loop used for writing / reading.
    
    file_path : `str`
        The location of the data base.
    
    spaces : `dict<int, list<int>>`
        Unused allocations.
    
    start_position : `int`
        Where the data base starts in the file.
    
    sync_io : `_io._IOBase`
        Io to use.
    
    write_queue : `None | list<(int, bytes)>`
        Location - data pairs.
    """
    __slots__ = (
        'end_position', 'end_position_real', 'entries', 'entry_count_allocated', 'entry_count_created', 'entry_type',
        'event_loop', 'file_path', 'spaces', 'start_position', 'sync_io', 'write_queue'
    )
    
    def __new__(
        cls,
        file_path,
        entry_type,
        event_loop,
        sync_io,
        start_position,
        end_position,
        entry_count_allocated,
        entry_count_created,
        entries,
        spaces,
    ):
        """
        Creates a new connected data base.
        
        Parameters
        ----------
        file_path : `str`
            The location of the data base.
            
        entry_type : ``EntryStructure``
            The held entries' type.
        
        event_loop : ``EventThread``
            Event loop used for writing / reading.
        
        sync_io : `_io._IOBase`
            Io to use.
        
        start_position : `int`
            Where the data base starts in the file.
        
        end_position : `int`
            Where the data base ends in the file.
        
        entry_count_allocated : `int`
            How much entries are allocated.
        
        entry_count_created : `int`
            How much entries were created.
        
        entries : `dict<int, .entry_type>`
            The entries of the data base.
        
        spaces : `dict<int, list<int>>`
            Unused allocations.
        """
        self = object.__new__(cls)
        self.end_position = end_position
        self.end_position_real = end_position
        self.entries = entries
        self.entry_count_allocated = entry_count_allocated
        self.entry_count_created = entry_count_created
        self.entry_type = entry_type
        self.event_loop = event_loop
        self.file_path = file_path
        self.spaces = spaces
        self.start_position = start_position
        self.sync_io = sync_io
        self.write_queue = None
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' file_path = ')
        repr_parts.append(repr(self.file_path))
        
        repr_parts.append(', entry_type = ')
        repr_parts.append(self.entry_type.__name__)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
