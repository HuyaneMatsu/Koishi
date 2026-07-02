import vampytest

from ..constants import DATABASE_READING_ERROR_CODE_END_OF_FILE, DATABASE_READING_ERROR_CODE_UNKNOWN_DATA_TYPE_ID
from ..data_base_reading_error import DataBaseReadingError


def test__DataBaseReadingError__new():
    """
    Tests whether ``DataBaseReadingError.__new__`` works as intended.
    """
    error_code = DATABASE_READING_ERROR_CODE_END_OF_FILE
    error_metadata = (0, 10)
    
    data_base_reading_error = DataBaseReadingError(error_code, error_metadata)
    
    vampytest.assert_instance(data_base_reading_error, DataBaseReadingError)
    vampytest.assert_instance(data_base_reading_error.error_code, int)
    vampytest.assert_instance(data_base_reading_error.error_metadata, tuple)
    
    vampytest.assert_eq(data_base_reading_error.error_code, error_code)
    vampytest.assert_eq(data_base_reading_error.error_metadata, error_metadata)


def test__DataBaseReadingError__repr():
    """
    Tests whether ``DataBaseReadingError.__repr__`` works as intended.
    """
    error_code = DATABASE_READING_ERROR_CODE_END_OF_FILE
    error_metadata = (0, 10)
    
    data_base_reading_error = DataBaseReadingError(error_code, error_metadata)
    
    output = repr(data_base_reading_error)
    vampytest.assert_instance(output, str)


def test__DataBaseReadingError__hash():
    """
    Tests whether ``DataBaseReadingError.__hash__`` works as intended.
    """
    error_code = DATABASE_READING_ERROR_CODE_END_OF_FILE
    error_metadata = (0, 10)
    
    data_base_reading_error = DataBaseReadingError(error_code, error_metadata)
    
    output = repr(data_base_reading_error)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    error_code = DATABASE_READING_ERROR_CODE_END_OF_FILE
    error_metadata = (0, 10)
    
    keyword_parameters = {
        'error_code': error_code,
        'error_metadata': error_metadata,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'error_metadata': (10, 1),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'error_code': DATABASE_READING_ERROR_CODE_UNKNOWN_DATA_TYPE_ID,
            'error_metadata': (10,),
        },
        False,
    )
    


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__DataBaseReadingError__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``DataBaseReadingError.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    data_base_reading_error_0 = DataBaseReadingError(**keyword_parameters_0)
    data_base_reading_error_1 = DataBaseReadingError(**keyword_parameters_1)
    
    output = data_base_reading_error_0 == data_base_reading_error_1
    vampytest.assert_instance(output, bool)
    return output
