import vampytest

from ..data_base_field import DataBaseField
from ..data_type import DataType
from ..data_types import STRING, UINT64


def _assert_fields_set(data_base_field):
    """
    Asserts whether every fields are set of the data base field.
    
    Parameters
    ----------
    data_base_field : ``DataBaseField``
        Instance to check.
    """
    vampytest.assert_instance(data_base_field, DataBaseField)
    vampytest.assert_instance(data_base_field.data_type, DataType)
    vampytest.assert_instance(data_base_field.name, str)


def test__DataBaseField__new():
    """
    Tests whether ``DataBaseField.__new__`` works as intended.
    """
    name = 'nyan'
    data_type = STRING
    
    data_base_field = DataBaseField(name, data_type)
    _assert_fields_set(data_base_field)
    
    vampytest.assert_eq(data_base_field.name, name)
    vampytest.assert_is(data_base_field.data_type, data_type)


def test__DataBaseField__repr():
    """
    Tests whether ``DataBaseField.__repr__`` works as intended.
    """
    name = 'nyan'
    data_type = STRING
    
    data_base_field = DataBaseField(name, data_type)
    
    output = repr(data_base_field)
    vampytest.assert_instance(output, str)


def test__DataBaseField__hash():
    """
    Tests whether ``DataBaseField.__hash__`` works as intended.
    """
    name = 'nyan'
    data_type = STRING
    
    data_base_field = DataBaseField(name, data_type)
    
    output = hash(data_base_field)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    name = 'nyan'
    data_type = STRING
    
    keyword_parameters = {
        'name' : name,
        'data_type' : data_type,
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
            'name' : 'rawr',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'data_type' : UINT64,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__DataBaseField__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``DataBaseField.__eq__`` works as intended.
    
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
    data_base_field_0 = DataBaseField(**keyword_parameters_0)
    data_base_field_1 = DataBaseField(**keyword_parameters_1)
    
    output = data_base_field_0 == data_base_field_1
    vampytest.assert_instance(output, bool)
    return output
