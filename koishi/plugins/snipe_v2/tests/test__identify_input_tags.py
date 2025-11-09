import vampytest

from ..responding_helpers import identify_input_tags


def _iter_options():
    yield (
        None,
        (
            True,
            None,
        ),
    )
    
    yield (
        '',
        (
            True,
            None,
        ),
    )
    
    yield (
        '    ',
        (
            True,
            None,
        ),
    )
    
    yield (
        '   ,  ',
        (
            True,
            None,
        ),
    )
    
    yield (
        'shrimp',
        (
            True,
            (
                'shrimp',
            ),
        ),
    )
    
    yield (
        'shrimp, fry',
        (
            True,
            (
                'fry',
                'shrimp',
            ),
        ),
    )
    
    yield (
        'shrimp, fry, fry',
        (
            True,
            (
                'fry',
                'shrimp',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__identify_input_tags(input_tags):
    """
    Identifies the passed tags.
    
    Parameters
    ----------
    input_tags : `str`
        Tags to identify.
    
    Returns
    -------
    output : `(bool, None | tuple<str>)`
    """
    output = identify_input_tags(input_tags)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    identified, tags = output
    vampytest.assert_instance(identified, bool)
    vampytest.assert_instance(tags, tuple, nullable = True)
    if (tags is not None):
        for element in tags:
            vampytest.assert_instance(element, str)
    
    return output
