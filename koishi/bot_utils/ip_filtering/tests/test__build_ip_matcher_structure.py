import vampytest

from ..ip_filter_rule import IPFilterRule
from ..ip_types import IP_TYPE_IP_V4
from ..node import Node
from ..utils import build_ip_matcher_structure


def _iter_options():
    yield (
        [],
        {},
    )
    
    yield (
        [
            IPFilterRule(IP_TYPE_IP_V4, 0xfff00000, 20),
            IPFilterRule(IP_TYPE_IP_V4, 0xf0f00000, 19),
        ],
        {
            IP_TYPE_IP_V4 : (
                Node(
                    None,
                    Node(
                        None,
                        Node(
                            None,
                            Node(
                                None,
                                Node(
                                    Node(
                                        Node(
                                            Node(
                                                Node(
                                                    None,
                                                    Node(
                                                        None,
                                                        Node(
                                                            None,
                                                            Node(
                                                                None,
                                                                Node(
                                                                    Node(
                                                                        None,
                                                                        None,
                                                                        True,
                                                                    ),
                                                                    None,
                                                                    False,
                                                                ),
                                                                False,
                                                            ),
                                                            False,
                                                        ),
                                                        False,
                                                    ),
                                                    False,
                                                ),
                                                None,
                                                False,
                                            ),
                                            None,
                                            False,
                                        ),
                                        None,
                                        False,
                                    ),
                                    Node(
                                        None,
                                        Node(
                                            None,
                                            Node(
                                                None,
                                                Node(
                                                    None,
                                                    Node(
                                                        None,
                                                        Node(
                                                            None,
                                                            Node(
                                                                None,
                                                                Node(
                                                                    None,
                                                                    None,
                                                                    True,
                                                                ),
                                                                False,
                                                            ),
                                                            False,
                                                        ),
                                                        False,
                                                    ),
                                                    False,
                                                ),
                                                False,
                                            ),
                                            False,
                                        ),
                                        False
                                    ),
                                    False,
                                ),
                                False,
                            ),
                            False,
                        ),
                        False,
                    ),
                    False,
                )
            ),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_ip_matcher_structure(rules):
    """
    Parameters
    ----------
    rules : ``iterable<IPFilterRule>``
        Rules to satisfy.
    
    Returns
    -------
    output : ``dict<int, Node>``
    """
    output = build_ip_matcher_structure(rules)
    
    vampytest.assert_instance(output, dict)
    for key, value in output.items():
        vampytest.assert_instance(key, int)
        vampytest.assert_instance(value, Node)
    
    return output
