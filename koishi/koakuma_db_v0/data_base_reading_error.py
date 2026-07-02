__all__ = ('DataBaseReadingError', )


def _produce_data_base_reading_error_message__end_of_file(data_base_reading_error):
    metadata = data_base_reading_error.error_metadata
    yield 'Reached end of file at position '
    yield repr(metadata[0])
    yield ', while still expecting to read '
    yield repr(metadata[1])
    yield ' more bytes.'


def _produce_data_base_reading_error_message__extended_length_byte_count_out_of_range(data_base_reading_error):
    metadata = data_base_reading_error.error_metadata
    yield 'Could not read '
    yield metadata[1].name
    yield '. Its length was supposedly stored on over 8 bytes; extended_length_byte_count = '
    yield repr(metadata[2])
    yield '; position_after_reading = '
    yield repr(metadata[0])
    yield '.'


def _produce_data_base_reading_error_message__unknown_data_type_id(data_base_reading_error):
    metadata = data_base_reading_error.error_metadata
    yield 'Unknown data type while reading data base header; data_type_id = '
    yield repr(metadata[0])
    yield '.'


def _produce_data_base_reading_error_message__field_empty_name(data_base_reading_error):
    yield 'A field in data base has empty name.'


def _produce_data_base_reading_error_message__fields_mismatch(data_base_reading_error):
    metadata = data_base_reading_error.error_metadata
    yield 'Database fields and the fields read mismatch; expected_fields = '
    yield repr(metadata[0])
    yield '; read_fields = '
    yield repr(metadata[1])
    yield '.'


DATA_BASE_READING_ERROR_MESSAGE_BUILDER = (
    None,
    _produce_data_base_reading_error_message__end_of_file,
    _produce_data_base_reading_error_message__extended_length_byte_count_out_of_range,
    _produce_data_base_reading_error_message__unknown_data_type_id,
    _produce_data_base_reading_error_message__field_empty_name,
    _produce_data_base_reading_error_message__fields_mismatch,
)


def get_data_base_reading_error_message_producer(error_code):
    """
    Gets error message producer.
    
    Parameters
    ----------
    error_code : `int`
        Parsing error code.
    
    Returns
    -------
    producer : `None | GeneratorType`
    """
    if (error_code >= 0) and (error_code < len(DATA_BASE_READING_ERROR_MESSAGE_BUILDER)):
        return DATA_BASE_READING_ERROR_MESSAGE_BUILDER[error_code]


class DataBaseReadingError(Exception):
    """
    Raised when data base reading is failing.
    
    Attributes
    ----------
    error_code : `int`
        The error's code identifying it.
    
    error_metadata : `tuple<object>`
        Additional metadata.
    """
    __slots__ = ('error_code', 'error_metadata')
    __init__ = object.__init__
    
    def __new__(cls, error_code, error_metadata):
        """
        Creates a new data base reading error.
        
        Parameters
        ----------
        error_code : `int`
            The error's code identifying it.
        
        error_metadata : `tuple<object>`
            Additional metadata.
        """
        self = Exception.__new__(cls)
        self.args = (error_code, error_metadata)
        self.error_code = error_code
        self.error_metadata = error_metadata
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        producer = get_data_base_reading_error_message_producer(self.error_code)
        if (producer is not None):
            repr_parts.append(' message = ')
            repr_parts.extend(producer(self))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.error_code != other.error_code:
            return False
        
        if self.error_metadata != other.error_metadata:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return self.error_code ^ hash(self.error_metadata)
