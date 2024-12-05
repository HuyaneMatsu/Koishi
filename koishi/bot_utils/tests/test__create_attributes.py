import vampytest

from ..instantiate_inheritance import create_attributes


def _iter_options__passing():
    yield (
        (
            'hey',
            'mister',
        ),
        {
            'nyan': 'orin',
        },
        (
            (
                ('hey', False, None),
                ('mister', False, None),
            ),
            {
                'nyan': 'orin',
            },
        ),
    )
    
    yield (
        (
            'hey',
            'mister',
        ),
        {
            'nyan': 'orin',
            'hey': 12
        },
        (
            (
                ('hey', True, 12),
                ('mister', False, None),
            ),
            {
                'nyan': 'orin',
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__create_attributes(slots, type_attributes):
    """
    Tests whether ``create_attributes`` works as intended.
    
    Parameters
    ----------
    slots : `tuple<str>`
        Slots defining the attribute listing.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Returns
    -------
    output : `tuple<(str, bool, object)>`
    type_attributes : `dict<str, object>`
    """
    type_attributes = type_attributes.copy()
    output = create_attributes(slots, type_attributes)
    vampytest.assert_instance(output, tuple)
    return output, type_attributes
