import vampytest

from ..utils import parse_ip, produce_ip_representation


def _iter_options():
    ip_string = f''
    yield (
        *parse_ip(ip_string),
        'unknown',
    )
    
    ip_string = f'{56:d}.{0:d}.{12:d}.{0:d}'
    yield (
        *parse_ip(ip_string),
        ip_string,
    )
    
    ip_string = f'{56:d}.{12:d}.{255:d}.{1:d}'
    yield (
        *parse_ip(ip_string),
        ip_string,
    )
    
    ip_string = f'{5612:x}:{12:x}:{255:x}:{1:x}:{0:x}:{2666:x}:{2626:x}:{2366:x}'
    
    yield (
        *parse_ip(ip_string),
        ip_string,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_ip_representation(ip_type, ip):
    """
    Tests whether ``produce_ip_representation`` works as intended.
    
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
    output = [*produce_ip_representation(ip_type, ip)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
