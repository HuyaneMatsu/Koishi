import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN

from ..rendering import is_self_target


def _iter_options():
    yield (
        None,
        None,
        None,
        False,
    )
    
    yield (
        {CHEN, YAKUMO_RAN},
        {'hug', 'kiss'},
        {'hey', 'mister'},
        False,
    )
    
    yield (
        {CHEN},
        {'hug'},
        {'hey'},
        False,
    )
    
    yield (
        {CHEN},
        {'hug'},
        None,
        False,
    )
    
    for tag in ('kon', 'stare'):
        yield (
            {CHEN},
            {tag},
            None,
            False,
        )
    
    for tag in ('feed_self', 'pocky_self'):
        yield (
            {CHEN},
            {tag},
            None,
            True,
        )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_self_target(characters, action_tags, unidentified):
    """
    Tests whether ``is_self_target`` works as intended.
    
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
    output = is_self_target(characters, action_tags, unidentified)
    vampytest.assert_instance(output, bool)
    return output
