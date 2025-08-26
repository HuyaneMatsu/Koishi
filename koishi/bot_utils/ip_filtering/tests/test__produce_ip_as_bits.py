import vampytest

from ..ip_types import IP_TYPE_IP_V4, IP_TYPE_IP_V6, IP_TYPE_NONE
from ..utils import produce_ip_as_bits

def _iter_options():
    yield (
        IP_TYPE_NONE,
        0,
        'unknown',
    )
    
    yield (
        IP_TYPE_IP_V4,
        (
            (56 << (8 * 3)) |
            (12 << (8 * 2)) |
            (255 << (8 * 1)) |
            (1 << (8 * 0))
        ),
        f'{56:0>8b}-{12:0>8b}-{255:0>8b}-{1:0>8b}',
    )
    
    yield (
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
        (
            f'{5612 >> 8:0>8b}-{5612 & 0xff:0>8b}-'
            f'{12 >> 8:0>8b}-{12 & 0xff:0>8b}-'
            f'{255 >> 8:0>8b}-{255 & 0xff:0>8b}-'
            f'{1 >> 8:0>8b}-{1 & 0xff:0>8b}-'
            f'{0 >> 8:0>8b}-{0 & 0xff:0>8b}-'
            f'{2666 >> 8:0>8b}-{2666 & 0xff:0>8b}-'
            f'{2626 >> 8:0>8b}-{2626 & 0xff:0>8b}-'
            f'{2366 >> 8:0>8b}-{2366 & 0xff:0>8b}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_ip_as_bits(ip_type, ip):
    """
    Tests whether ``produce_ip_as_bits`` works as intended.
    
    Parameters
    ----------
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        Ip value.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_ip_as_bits(ip_type, ip)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
