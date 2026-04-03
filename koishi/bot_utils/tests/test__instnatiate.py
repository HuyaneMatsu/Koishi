import vampytest

from ..instantiate_inheritance import instantiate


class TestType():
    __slots__ = ('hey', 'mister')
    
    def __new__(cls, hey, mister):
        self = object.__new__(cls)
        self.hey = hey
        self.mister = mister
        return self
    
    def __eq__(self, other):
        return self.hey == other.hey and self.mister == other.mister


def _iter_options():
    yield (
        TestType,
        (
            ('hey', True, 10),
            ('mister', True, 12),
        ),
        {},
        TestType(10, 12),
    )
    
    yield (
        TestType,
        (
            ('hey', True, 13),
            ('mister', False, None),
        ),
        {
            'mister': 12,
        },
        TestType(13, 12),
    )
    
    yield (
        TestType,
        (
            ('hey', False, None),
            ('mister', False, None),
        ),
        {
            'hey': 15,
            'mister': 14,
        },
        TestType(15, 14)
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__instantiate(direct_parent, attributes, type_attributes):
    """
    Tests whether ``instantiate`` works as intended.
    
    Parameters
    ----------
    direct_parent : `type`
        Type to instantiate.
    
    attributes : `tuple<(str, bool, object)>`
        Attributes to check with.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Returns
    -------
    output : instance<direct_parent>`
    """
    output = instantiate(direct_parent, attributes, type_attributes)
    vampytest.assert_instance(output, direct_parent)
    return output
