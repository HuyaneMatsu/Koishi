import vampytest

from ..instantiate_inheritance import check_parameter_omitted


def _iter_options__passing():
    yield (
        (),
        {},
    )
    
    yield (
        (
            ('hey', True, 10),
            ('mister', True, 12),
        ),
        {},
    )
    
    yield (
        (
            ('hey', True, 13),
            ('mister', False, None),
        ),
        {
            'mister': 12,
        },
    )
    
    yield (
        (
            ('hey', False, None),
            ('mister', False, None),
        ),
        {
            'hey': 12,
            'mister': 12,
        },
    )


def _iter_options__type_error():
    yield (
        (
            ('hey', True, None),
            ('mister', False, None),
        ),
        {},
    )
    
    yield (
        (
            ('hey', False, None),
            ('mister', False, None),
        ),
        {
            'hey': 12,
        },
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__check_parameter_omitted(attributes, type_attributes):
    """
    Tests whether ``check_parameter_omitted`` works as intended.
    
    Parameters
    ----------
    attributes : `tuple<(str, bool, object)>`
        Attributes to check with.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Raises
    ------
    TypeError
    """
    return check_parameter_omitted(attributes, type_attributes)
