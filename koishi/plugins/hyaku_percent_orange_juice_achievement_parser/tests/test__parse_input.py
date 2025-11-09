import vampytest

from ..logic import parse_input


def _iter_options():
    yield (
        (
            '\n'
            'Pudding Chaser\n'
            'Complete QP\'s Scenario on Normal Difficulty or Higher\n'
            'Unlocked 24 Apr @ 8:39pm\n'
            'Hyper\n'
            'Complete Suguri\'s Scenario on Normal Difficulty or Higher\n'
            'Unlocked 3 Nov, 2024 @ 11:12am\n'
            'A Little Aviator\n'
            'Complete Marc\'s Scenario on Normal Difficulty or Higher\n'
            'Unlocked 6 Jun @ 10:40pm\n'
        ),
        {
            'Pudding Chaser',
            'Hyper',
            'A Little Aviator',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_input(content):
    """
    Parses the input content.
    
    Parameters
    ----------
    content : `str`
        Content to parse.
    
    Returns
    -------
    output : `set<str>`
    """
    output = parse_input(content)
    
    vampytest.assert_instance(output, set)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
