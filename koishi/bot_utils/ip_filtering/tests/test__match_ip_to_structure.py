import vampytest

from ..ip_filter_rule import IPFilterRule
from ..ip_types import IP_TYPE_IP_V4, IP_TYPE_IP_V6
from ..utils import build_ip_matcher_structure, match_ip_to_structure, parse_ip


def _iter_options():
    structure_0 =  build_ip_matcher_structure([
        IPFilterRule(IP_TYPE_IP_V4, 0xfff00000, 20),
        IPFilterRule(IP_TYPE_IP_V4, 0xf0f00000, 19),
    ])
    
    yield (
        structure_0,
        IP_TYPE_IP_V4,
        0xfffa1234,
        True,
    )
    
    yield (
        structure_0,
        IP_TYPE_IP_V4,
        0xfafa1234,
        False,
    )
    
    yield (
        structure_0,
        IP_TYPE_IP_V6,
        0xfffa1234,
        False,
    )
    
    # More practical cases
    ip_structure_1 =  build_ip_matcher_structure([
        IPFilterRule(*parse_ip('54.243.127.66'), 16),
        IPFilterRule(*parse_ip('54.87.227.43'), 16),
    ])
    
    yield (
        ip_structure_1,
        *parse_ip('54.243.186.148'),
        True,
    )
    
    yield (
        ip_structure_1,
        *parse_ip('54.81.117.136'),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__match_ip_to_structure(structure, ip_type, ip):
    """
    Tests whether ``match_ip_to_structure`` works as intended.
    
    Parameters
    ----------
    structure : ``dict<int, Node>``
        Structure to be matched.
    
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        The ip address.
    
    Returns
    -------
    output : `bool`
    """
    output = match_ip_to_structure(structure, ip_type, ip)
    vampytest.assert_instance(output, bool)
    return output
