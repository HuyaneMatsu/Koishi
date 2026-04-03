import vampytest

from ..helpers import get_time_zone_suggestions


def _iter_options():
    yield (
        None,
        [
            'Africa/Cairo (+02:00)',
            'Africa/Douala (+01:00)',
            'Africa/Harare (+02:00)',
            'America/Anchorage (-09:00)',
            'America/Aruba (-04:00)',
            'America/Bogota (-05:00)',
            'America/Buenos Aires (-03:00)',
            'America/Caracas (-04:30)',
            'America/Chicago (-06:00)',
            'America/Denver (-07:00)',
            'America/Godthab (-03:00)',
            'America/Halifax (-05:00)',
            'America/Los Angeles (-08:00)',
            'America/Mazatlan (-07:00)',
            'America/Mexico City (-06:00)',
            'America/Montevideo (-03:00)',
            'America/New York (-05:00)',
            'America/Phoenix (-07:00)',
            'America/Sao Paulo (-03:00)',
            'Asia/Baghdad (+03:00)',
            'Asia/Baku (+04:00)',
            'Asia/Bangkok (+07:00)',
            'Asia/Chennai (+05:30)', 
            'Asia/Dhaka (+06:00)',
            'Asia/Hong Kong (+08:00)',
        ],
    )
    
    yield (
        'afri',
        [
            'Africa/Cairo (+02:00)',
            'Africa/Douala (+01:00)',
            'Africa/Harare (+02:00)',
        ],
    )
    
    yield (
        'cai',
        [
            'Africa/Cairo (+02:00)',
            'America/Buenos Aires (-03:00)',
            'America/Chicago (-06:00)',
            'America/Halifax (-05:00)',
            'America/Mexico City (-06:00)',
            'America/Montevideo (-03:00)',
            'America/Phoenix (-07:00)',
            'Asia/Chennai (+05:30)',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_time_zone_suggestions(name):
    """
    Tests whether ``get_time_zone_suggestions`` works as intended.
    
    Parameters
    ----------
    name : `None | str`
        Time zone name.
    
    Returns
    -------
    output : `list<str>`
    """
    output = get_time_zone_suggestions(name)
    vampytest.assert_instance(output, list)
    return output
