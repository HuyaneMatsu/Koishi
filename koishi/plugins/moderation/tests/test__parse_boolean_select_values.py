import vampytest

from ..helpers import parse_boolean_select_values


def _iter_options():
    yield (
        None,
        False,
        False,
    )
    
    yield (
        None,
        True,
        True,
    )
    
    yield (
        ('0',),
        False,
        False,
    )
    
    yield (
        ('0',),
        True,
        False,
    )
    
    yield (
        ('1',),
        False,
        True,
    )
    
    yield (
        ('1',),
        True,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_boolean_select_values(values, default):
    """
    Tests whether ``parse_boolean_select_values`` works as intended.
    
    Parameters
    ----------
    values : `None | tuple<str>`
        The selected value(s).
    
    default : `bool`
        Default value to return if none is received.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_boolean_select_values(values, default)
    vampytest.assert_instance(output, bool)
    return output
