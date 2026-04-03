import vampytest

from ....bot_utils.ip_filtering import IP_TYPE_IP_V4

from ..logic import get_entry_for_ip


def _iter_options():
    entry_0 = (
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
    )
    
    yield (
        [
            entry_0,
        ],
        IP_TYPE_IP_V4,
        (1 << 24) | (0 << 16) | (128 << 8) | (1 << 0),
        entry_0,
    )
    
    yield (
        [
            entry_0,
        ],
        IP_TYPE_IP_V4,
        (1 << 24) | (1 << 16) | (128 << 8) | (0 << 0),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_entry_for_ip(entries, ip_type, ip):
    """
    Tests whether ``get_entry_for_ip`` works as intended.
    
    Parameters
    ----------
    entries : `list<(int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)>`
        Entries to select from.
    
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        The ip's value.
    
    Returns
    -------
    output : `None | (int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)`
    """
    output = get_entry_for_ip(entries, ip_type, ip)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
