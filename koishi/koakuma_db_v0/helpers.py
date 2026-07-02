__all__ = ()

from .constants import DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE
from .data_base_reader import data_base_reader_read
from .data_base_reading_error import DataBaseReadingError


def get_string_encoded_length(string):
    """
    Gets a string's encoded length.
    
    Parameters
    ----------
    string : `None | str`
        The string to get its encoded length of.
    
    Returns
    -------
    encoded_length : `int`
    """
    string_encoded_length = 0
    
    if (string is not None):
        for character in string:
            character_int = ord(character)
            if character_int >= 0x10000 or character_int < 0:
                character_encoded_length = 4
            
            elif character_int >= 0x100:
                character_encoded_length = 2
            
            else:
                character_encoded_length = 1
            
            string_encoded_length += character_encoded_length
    
    return string_encoded_length


def get_length_encoded_byte_count(length):
    """
    Gets how much bytes it requires to encode the given length.
    
    Parameters
    ----------
    length : `int`
        The length to work with.
    
    Returns
    -------
    byte_count : `int`
    """
    byte_count = 1
    if length > 63:
        byte_count += convert_length_to_extended_length_byte_count(length)
    
    return byte_count


def convert_length_to_extended_length_byte_count(length):
    """
    Convert a length to length extension length.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    byte_count : `int`
    """
    byte_count = 0
    while length:
        byte_count += 1
        length >>= 8
    
    return byte_count


def produce_length_bytes(length):
    """
    Produces length bytes.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Yields
    ------
    part : `bytes`
    """
    if length < 64:
       yield length.to_bytes(1, 'little')
    else:
        extended_length_byte_count = convert_length_to_extended_length_byte_count(length)
        yield (64 | extended_length_byte_count).to_bytes(1, 'little')
        yield length.to_bytes(extended_length_byte_count, 'little')


def build_length_bytes(length):
    """
    Builds length bytes.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    length_bytes : `bytes`
    """
    if length < 64:
        length_bytes = length.to_bytes(1, 'little')
    else:
        extended_length_byte_count = convert_length_to_extended_length_byte_count(length)
        length_bytes = (
            (64 | extended_length_byte_count).to_bytes(1, 'little') +
            length.to_bytes(extended_length_byte_count, 'little')
        )
    
    return length_bytes


def build_space_bytes(length):
    """
    Builds space bytes.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    space_bytes : `bytes`
    """
    if length < 64:
        length_bytes = (128 | length).to_bytes(1, 'little')
    else:
        extended_length_byte_count = convert_length_to_extended_length_byte_count(length)
        length_bytes = (
            (192 | extended_length_byte_count).to_bytes(1, 'little') +
            length.to_bytes(extended_length_byte_count, 'little')
        )
    
    return length_bytes


# Structure
# bit
# | 7        | 6               | 5 | 4 | 3 | 2 | 1 | 0 |
# | reserved | extended length | length                |

async def read_length(data_base_reader, data_type):
    """
    Reads generic length.
    
    This function is a coroutine.
    
    Parameters
    ----------
    data_base_reader : ``DataBaseReader``
        Data base reader to use.
    
    data_type : ``DataType``
        The current data type to be read.
    
    Returns
    -------
    length : `int`
    """
    data = await data_base_reader_read(data_base_reader, 1)
    length = data[0]
    if not length:
        return 0
    
    extended_length = length & 64
    length &= 63
    
    if extended_length:
        if length > 8:
            raise DataBaseReadingError(
                DATABASE_READING_ERROR_CODE_EXTENDED_LENGTH_BYTE_COUNT_OUT_OF_RANGE,
                (data_base_reader.position, data_type, length),
            )
        
        data = await data_base_reader_read(data_base_reader, length)
        length = int.from_bytes(data, 'little')
    
    return length
