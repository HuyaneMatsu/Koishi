import vampytest

from ..node import Node


def _assert_fields_set(node):
    """
    Asserts whether every fields are set of the given node.
    
    Parameters
    ----------
    node : ``Node``
        The instance to check.
    """
    vampytest.assert_instance(node, Node)
    vampytest.assert_instance(node.absorb, bool)
    vampytest.assert_instance(node.one, Node, nullable = True)
    vampytest.assert_instance(node.zero, Node, nullable = True)


def test__Node__new():
    """
    Tests whether ``Node.__new__`` works as intended.
    """
    zero = Node(None, None, True)
    one = Node(None, None, False)
    absorb = False
    
    node = Node(
        zero,
        one,
        absorb,
    )
    _assert_fields_set(node)
    
    vampytest.assert_eq(node.absorb, absorb)
    vampytest.assert_eq(node.one, one)
    vampytest.assert_eq(node.zero, zero)


def test__Node__repr():
    """
    Tests whether ``Node.__repr__`` works as intended.
    """
    zero = Node(None, None, True)
    one = Node(None, None, False)
    absorb = False
    
    node = Node(
        zero,
        one,
        absorb,
    )
    
    output = repr(node)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    zero = Node(None, None, True)
    one = Node(None, None, False)
    absorb = False
    
    keyword_parameters = {
        'zero' : zero,
        'one': one,
        'absorb' : absorb,
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
            'zero': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'one': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'absorb': True,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Node__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Node.__eq__`` works as intended.
    
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
    node_0 = Node(**keyword_parameters_0)
    node_1 = Node(**keyword_parameters_1)
    
    output = node_0 == node_1
    vampytest.assert_instance(output, bool)
    return output


def test__Node__hash():
    """
    Tests whether ``Node.__hash__`` works as intended.
    """
    zero = Node(None, None, True)
    one = Node(None, None, False)
    absorb = False
    
    node = Node(
        zero,
        one,
        absorb,
    )
    
    output = hash(node)
    vampytest.assert_instance(output, int)
