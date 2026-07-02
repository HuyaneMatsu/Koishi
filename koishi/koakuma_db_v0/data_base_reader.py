__all__ = ()

from functools import partial as partial_function
from scarletio import RichAttributeErrorBaseType

from .constants import FILE_READ_CHUNK_SIZE, DATABASE_READING_ERROR_CODE_END_OF_FILE
from .data_base_reading_error import DataBaseReadingError


def _seek_and_read(sync_io, position):
    """
    Seeks at the given start position and reads a chunk of data.
    
    Parameters
    ----------
    sync_io : `_io._IOBase`
        Io to use.
    
    position : `int`
        Position to start reading at.
    """
    sync_io.seek(position)
    return sync_io.read(FILE_READ_CHUNK_SIZE)


def data_base_reader_begin(data_base_reader, position):
    """
    Begins reading the data base at the given position.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to operate on.
    
    position : `int`
        Position to start reading at.
    """
    data_base_reader.position = position
    data_base_reader.future = data_base_reader.event_loop.run_in_executor(
        partial_function(_seek_and_read, data_base_reader.sync_io, position)
    )


def data_base_reader_abort(data_base_reader):
    """
    Aborts the current reading action of the data base reader.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to operate on.
    """
    data_base_reader.chunk = None
    future = data_base_reader.future
    if (future is not None):
        data_base_reader.future = None
        future.cancel()


async def data_base_reader_get_chunk(data_base_reader):
    """
    Gets the next chunk that the data base has read and sets a new reader future.
    
    This function is a coroutine.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to operate on.
    
    Returns
    -------
    chunk : `None | bytes`
    """
    future = data_base_reader.future
    if future is None:
        chunk = None
    else:
        chunk = await future
        if len(chunk) != FILE_READ_CHUNK_SIZE:
            future = None
        else:
            sync_io = data_base_reader.sync_io
            future = data_base_reader.event_loop.run_in_executor(
                partial_function(type(sync_io).read, sync_io, FILE_READ_CHUNK_SIZE)
            )
        
        data_base_reader.future = future
    
    return chunk


async def data_base_reader_read(data_base_reader, length):
    """
    Reads data of the given length.
    
    This function is a coroutine.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to operate on.
    
    length : `int`
        Amount of bytes to read.
    
    Returns
    -------
    data : `bytes | memoryview`
    
    Raises
    ------
    DataBaseReadingError
    """
    chunk = data_base_reader.chunk
    if (chunk is not None):
        chunk_start = data_base_reader.chunk_start
        chunk_length = data_base_reader.chunk_length
    
    else:
        chunk = await data_base_reader_get_chunk(data_base_reader)
        if chunk is None:
            data_base_reader_abort(data_base_reader)
            raise DataBaseReadingError(
                DATABASE_READING_ERROR_CODE_END_OF_FILE,
                (data_base_reader.position, length),
            )
        
        data_base_reader.chunk_length = chunk_length = len(chunk)
        data_base_reader.chunk_start = chunk_start = 0
        chunk = memoryview(chunk)
        data_base_reader.chunk = chunk
    
    end = chunk_start + length
    if end <= chunk_length:
        data = chunk[chunk_start : end]
        if end < chunk_length:
            data_base_reader.chunk_start = end
        else:
            data_base_reader.chunk = None
    
    else:
        parts = [chunk[chunk_start : chunk_length]]
        to_collect = length + chunk_start - chunk_length
        
        while True:
            chunk = await data_base_reader_get_chunk(data_base_reader)
            if chunk is None:
                data_base_reader_abort(data_base_reader)
                raise DataBaseReadingError(
                    DATABASE_READING_ERROR_CODE_END_OF_FILE,
                    (data_base_reader.position, length),
                )
                
            chunk_length = len(chunk)
            chunk = memoryview(chunk)
            
            if to_collect <= chunk_length:
                parts.append(chunk[: to_collect])
                if to_collect == chunk_length:
                    chunk = None
                break
            
            parts.append(chunk)
            to_collect -= chunk_length
            continue
        
        data = b''.join(parts)
        
        data_base_reader.chunk = chunk
        data_base_reader.chunk_start = to_collect
        data_base_reader.chunk_length = chunk_length
    
    data_base_reader.position += length
    
    return data


async def data_base_reader_skip(data_base_reader, length):
    """
    Skips data of the given length.
    
    This function is a coroutine.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to operate on.
    
    length : `int`
        Amount of bytes to read.
    
    Raises
    ------
    DataBaseReadingError
    """
    chunk = data_base_reader.chunk
    if (chunk is not None):
        chunk_start = data_base_reader.chunk_start
        chunk_length = data_base_reader.chunk_length
    
    else:
        chunk = await data_base_reader_get_chunk(data_base_reader)
        if chunk is None:
            data_base_reader_abort(data_base_reader)
            raise DataBaseReadingError(
                DATABASE_READING_ERROR_CODE_END_OF_FILE,
                (data_base_reader.position, length),
            )
        
        data_base_reader.chunk_length = chunk_length = len(chunk)
        data_base_reader.chunk_start = chunk_start = 0
        chunk = memoryview(chunk)
        data_base_reader.chunk = chunk
    
    end = chunk_start + length
    if end <= chunk_length:
        if end < chunk_length:
            data_base_reader.chunk_start = end
        else:
            data_base_reader.chunk = None
    
    else:
        to_collect = length + chunk_start - chunk_length
        
        while True:
            chunk = await data_base_reader_get_chunk(data_base_reader)
            if chunk is None:
                data_base_reader_abort(data_base_reader)
                raise DataBaseReadingError(
                    DATABASE_READING_ERROR_CODE_END_OF_FILE,
                    (data_base_reader.position, length),
                )
                
            chunk_length = len(chunk)
            chunk = memoryview(chunk)
            
            if to_collect <= chunk_length:
                if to_collect == chunk_length:
                    chunk = None
                break
            
            to_collect -= chunk_length
            continue
        
        data_base_reader.chunk = chunk
        data_base_reader.chunk_start = to_collect
        data_base_reader.chunk_length = chunk_length
    
    data_base_reader.position += length


class DataBaseReader(RichAttributeErrorBaseType):
    """
    Represents a data base reader.
    
    Attributes
    ----------
    chunk : `None | memoryview`
        The current chunk being processed.
    
    chunk_start : `int`
        The starting position of the chunk the next read should start at.
    
    chunk_length : `int`
        The length of the chunk.
    
    event_loop : ``EventThead``
        Event loop to use.
    
    future : `` None | Future``
        Chunk waiter future.
    
    position : `int`
        Absolute position.
    
    sync_io : `_io._IOBase`
        Io to use.
    """
    __slots__ = ('chunk', 'chunk_start', 'chunk_length', 'event_loop', 'future', 'position', 'sync_io')
    
    def __new__(cls, event_loop, sync_io):
        """
        Creates a new data base reader.
        
        Parameters
        ----------
        event_loop : ``EventThread``
            Event loop to operate on.
        
        sync_io : `_io._IOBase`
            Io to use.
        """
        self = object.__new__(cls)
        self.chunk = None
        self.chunk_start = 0
        self.chunk_length = 0
        self.event_loop = event_loop
        self.position = 0
        self.future = None
        self.sync_io = sync_io
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(', event_loop = ')
        repr_parts.append(repr(self.event_loop))
        
        repr_parts.append(', sync_io = ')
        repr_parts.append(repr(self.sync_io))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
