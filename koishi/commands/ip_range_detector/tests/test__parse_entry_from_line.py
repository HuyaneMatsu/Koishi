import vampytest

from ....bot_utils.ip_filtering import IP_TYPE_IP_V4

from ..logic import parse_entry_from_line


def _iter_options():
    yield (
        (
            '{"network": "1.0.128.0/17", "country": "Thailand", "country_code": "TH", "continent": "Asia", '
            '"continent_code": "AS", "asn": "AS23969", "as_name": "TOT Public Company Limited", '
            '"as_domain": "ntplc.co.th"}'
        ),
        (
            IP_TYPE_IP_V4,
            (1 << 24) | (0 << 16) | (128 << 8) | (0 << 0),
            15,
            'Thailand',
            'TH',
            'Asia',
            'AS',
            'AS23969',
            'TOT Public Company Limited',
            'ntplc.co.th',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entry_from_line(line):
    """
    Tests whether ``parse_entry_from_line`` works as intended.
    
    Parameters
    ----------
    line : `str`
        Line to parse.
    
    Returns
    --------
    output : `None | (int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)`
    """
    string_cache = {}
    output = parse_entry_from_line(line, string_cache)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
