import vampytest

from ..ip_filter_rule import IPFilterRule
from ..ip_types import IP_TYPE_IP_V4, IP_TYPE_IP_V6


def _assert_fields_set(ip_filter_rule):
    """
    Asserts whether every fields are set of the given rule.
    
    Parameters
    ----------
    ip_filter_rule : ``IPFilterRule``
        Rule to check.
    """
    vampytest.assert_instance(ip_filter_rule, IPFilterRule)
    vampytest.assert_instance(ip_filter_rule.absorbed_bits, int)
    vampytest.assert_instance(ip_filter_rule.ip, int)
    vampytest.assert_instance(ip_filter_rule.type, int)


def test__IPFilterRule__new():
    """
    Tests whether ``IPFilterRule.__new__`` works as intended.
    """
    absorbed_bits = 12
    ip = 0x12563296
    ip_type = IP_TYPE_IP_V4
    
    ip_filter_rule = IPFilterRule(
        ip_type,
        ip,
        absorbed_bits,
    )
    
    vampytest.assert_eq(ip_filter_rule.absorbed_bits, absorbed_bits)
    vampytest.assert_eq(ip_filter_rule.ip, ip)
    vampytest.assert_eq(ip_filter_rule.type, ip_type)


def test__IPFilterRule__repr():
    """
    Tests whether ``IPFilterRule.__repr__`` works as intended.
    """
    absorbed_bits = 12
    ip = 0x12563296
    ip_type = IP_TYPE_IP_V4
    
    ip_filter_rule = IPFilterRule(
        ip_type,
        ip,
        absorbed_bits,
    )
    
    output = repr(ip_filter_rule)
    vampytest.assert_instance(output, str)
    return output


def _iter_options__eq():
    absorbed_bits = 12
    ip = 0x12563296
    ip_type = IP_TYPE_IP_V4
    
    keyword_parameters = {
        'ip_type' : ip_type,
        'ip' : ip,
        'absorbed_bits' : absorbed_bits,
    }
    
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'ip_type' : IP_TYPE_IP_V6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'ip' : 0x12563290,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'absorbed_bits' : 10,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__IPFilterRule__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``IPFilterRule.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    ip_filter_rule_0 = IPFilterRule(**keyword_parameters_0)
    ip_filter_rule_1 = IPFilterRule(**keyword_parameters_1)
    
    output = ip_filter_rule_0 == ip_filter_rule_1
    vampytest.assert_instance(output, bool)
    return output


def test__IPFilterRule__hash():
    """
    Tests whether ``IPFilterRule.__hash__`` works as intended.
    """
    absorbed_bits = 12
    ip = 0x12563296
    ip_type = IP_TYPE_IP_V4
    
    ip_filter_rule = IPFilterRule(
        ip_type,
        ip,
        absorbed_bits,
    )
    
    output = hash(ip_filter_rule)
    vampytest.assert_instance(output, int)
    return output
