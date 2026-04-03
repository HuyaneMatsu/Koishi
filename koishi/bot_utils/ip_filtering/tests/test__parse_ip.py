import vampytest

from ..ip_types import IP_TYPE_IP_V4, IP_TYPE_IP_V6, IP_TYPE_NONE
from ..utils import parse_ip


def _iter_options():
    yield (
        '',
        (
            IP_TYPE_NONE,
            0,
        ),
    )
    
    yield (
        f'{56:d}.{12:d}.{255:d}.{1:d}',
        (
            IP_TYPE_IP_V4,
            (
                (56 << (8 * 3)) |
                (12 << (8 * 2)) |
                (255 << (8 * 1)) |
                (1 << (8 * 0))
            ),
        ),
    )
    
    yield (
        f'{5612:x}:{12:x}:{255:x}:{1:x}:{0:x}:{2666:x}:{2626:x}:{2366:x}',
        (
            IP_TYPE_IP_V6,
            (
                (5612 << (16 * 7)) |
                (12 << (16 * 6)) |
                (255 << (16 * 5)) |
                (1 << (16 * 4)) |
                (0 << (16 * 3)) |
                (2666 << (16 * 2)) |
                (2626 << (16 * 1)) |
                (2366 << (16 * 0))
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_ip(ip_string):
    """
    Tests whether ``parse_ip`` works as intended.
    
    Parameters
    ----------
    ip_string : `str`
        Value to test with.
    
    Returns
    -------
    output : `(int, int)`
    """
    output = parse_ip(ip_string)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], int)
    return output
