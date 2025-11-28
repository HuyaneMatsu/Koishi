__all__ = ('build_ip_matcher_structure', 'match_ip_to_structure', 'parse_ip', 'produce_ip_representation')

from re import compile as re_compile

from .ip_types import IP_TYPE_IP_V4, IP_TYPE_IP_V6, IP_TYPE_NONE
from .node import Node


IP_V4_UNIT = '([0-9]|[1-9][0-9]|1[0-9][0-9]|2(?:[0-4][0-9]|5[0-5]))'
IP_V6_UNIT = '([0-9a-f]{1,4})'
IP_V4_RP = re_compile(
    f'{IP_V4_UNIT}\\.{IP_V4_UNIT}\\.{IP_V4_UNIT}\\.{IP_V4_UNIT}'
)
IP_V6_RP = re_compile(
    f'{IP_V6_UNIT}\\:{IP_V6_UNIT}\\:{IP_V6_UNIT}\\:{IP_V6_UNIT}\\:'
    f'{IP_V6_UNIT}\\:{IP_V6_UNIT}\\:{IP_V6_UNIT}\\:{IP_V6_UNIT}'
)


def parse_ip(ip_string):
    """
    Parses the given ip string to an ip-type & ip value pair.
    
    Parameters
    ----------
    ip_string : `str`
        Ip value to parse.
    
    Returns
    -------
    ip_type_and_ip : `(int, int)`
    """
    while True:
        ip = 0
        
        match = IP_V4_RP.fullmatch(ip_string)
        if (match is not None):
            ip_type = IP_TYPE_IP_V4
            for value, shift in zip(match.groups(), range(24, -8, -8)):
                ip |= int(value) << shift
            break
        
        match = IP_V6_RP.fullmatch(ip_string)
        if (match is not None):
            ip_type = IP_TYPE_IP_V6
            for value, shift in zip(match.groups(), range(112, -16, -16)):
                ip |= int(value, 16) << shift
            break
        
        ip_type = IP_TYPE_NONE
        break
    
    return ip_type, ip


def produce_ip_as_bits(ip_type, ip):
    """
    Produces the given ip-type and ip as bits.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        Ip value.
    
    Yields
    ------
    part : `str`
    """
    if ip_type == IP_TYPE_IP_V4:
        ip_size = 32
    
    elif ip_type == IP_TYPE_IP_V6:
        ip_size = 128
    
    else:
        yield 'unknown'
        return
    
    for shift in range(ip_size -8, -8, -8):
        yield format(((ip >> shift) & 0xff), '0>8b')
        if shift:
            yield '-'


def produce_ip_representation(ip_type, ip):
    """
    Produces the ip's representation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        Ip value.
    
    Yields
    ------
    part : `str`
    """
    if ip_type == IP_TYPE_IP_V4:
        ip_size = 32
        unit_size = 8
        mode = 'd'
        separator = '.'
    
    elif ip_type == IP_TYPE_IP_V6:
        ip_size = 128
        unit_size = 16
        mode = 'x'
        separator = ':'
    
    else:
        yield 'unknown'
        return
    
    mask = (1 << unit_size) - 1
    for shift in range(ip_size -unit_size, -unit_size, -unit_size):
        yield format((ip >> shift) & mask, mode)
        if shift:
            yield separator


def build_ip_matcher_structure(rules):
    """
    Builds a an ip matcher structure.
    
    Parameters
    ----------
    rules : ``iterable<IPFilterRule>``
        Rules to satisfy.
    
    Returns
    -------
    structure : ``dict<int, Node>``
    """
    by_type = {}
    
    for rule in rules:
        ip_type = rule.type
        
        try:
            node = by_type[ip_type]
        except KeyError:
            node = Node(None, None, False)
            by_type[ip_type] = node
        
        if ip_type == IP_TYPE_IP_V4:
            ip_size = 32
        else:
            ip_size = 128
        
        value = rule.ip
        
        for shift in range(ip_size - 1, rule.absorbed_bits - 1, -1):
            bit = (value >> shift) & 1
            
            if bit:
                sub_node = node.one
            else:
                sub_node = node.zero
            
            if sub_node is None:
                sub_node = Node(None, None, False)
                if bit:
                    node.one = sub_node
                else:
                    node.zero = sub_node
            
            else:
                if sub_node.absorb:
                    break
            
            node = sub_node
        
        else:
            node.absorb = True
        
        continue
    
    return by_type


def match_ip_to_structure(structure, ip_type, ip):
    """
    Matches the given ip-type and ip to the given structure.
    
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
    matched : `bool`
    """
    try:
        node = structure[ip_type]
    except KeyError:
        return False
    
    if ip_type == IP_TYPE_IP_V4:
        ip_size = 32
    else:
        ip_size = 128
    
    for shift in range(ip_size - 1, - 1, -1):
        bit = (ip >> shift) & 1
        
        if bit:
            sub_node = node.one
        else:
            sub_node = node.zero
        
        if sub_node is None:
            return False
        
        if sub_node.absorb:
            return True
        
        node = sub_node
        continue
    
    return False
