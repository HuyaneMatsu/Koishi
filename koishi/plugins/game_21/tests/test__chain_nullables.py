import vampytest

from ..helpers import chain_nullables


def _iter_options():
    yield (), []
    yield (None, None), []
    yield (None, [1, 2]), [1, 2]
    yield ([1, 2], None), [1, 2]
    yield ([1, 2], [3, 4]), [1, 2, 3, 4]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__chain_nullables(nullable_iterables):
    """
    Tests whether ``chain_nullables`` works as intended.
    
    Parameters
    ----------
    nullable_iterables : `tuple<iterable>`
        Iterables to chain.
    
    Returns
    -------
    output : `list`
    """
    return [*chain_nullables(*nullable_iterables)]
