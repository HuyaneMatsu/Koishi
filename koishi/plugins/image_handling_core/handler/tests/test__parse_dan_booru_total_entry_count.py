import vampytest

from ..dan_booru import parse_dan_booru_total_entry_count


def _iter_options():
    yield (
        None,
        0,
    )
    
    yield (
        {
            'counts': {
                'posts': 23,
            },
        },
        23,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_dan_booru_total_entry_count(data):
    """
    Tests whether ``parse_dan_booru_total_entry_count`` works as intended.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_dan_booru_total_entry_count(data)
    vampytest.assert_instance(output, int)
    return output
