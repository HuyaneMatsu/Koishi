import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN

from ..rendering import is_cross_target


def _iter_options():
    yield (
        None,
        None,
        None,
        False,
    )
    
    yield (
        {CHEN, YAKUMO_RAN},
        {'handhold', 'kiss'},
        None,
        False,
    )
    
    yield (
        {CHEN, YAKUMO_RAN},
        {'handhold'},
        {'hey'},
        False,
    )
    
    yield (
        {CHEN, YAKUMO_RAN},
        {'kiss'},
        None,
        False,
    )
    
    for tag in ('handhold',):
        yield (
            {CHEN, YAKUMO_RAN},
            {tag},
            None,
            True,
        )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_cross_target(characters, action_tags, unidentified):
    """
    Tests whether ``is_cross_target`` works as intended.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    output : `bool`
    """
    output = is_cross_target(characters, action_tags, unidentified)
    vampytest.assert_instance(output, bool)
    return output
