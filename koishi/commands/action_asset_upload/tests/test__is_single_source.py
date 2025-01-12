import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN

from ..rendering import is_single_source


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
            True,
        )
    
    for tag in ('feed_self', 'pocky_self'):
        yield (
            {CHEN},
            {tag},
            None,
            False,
        )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_single_source(characters, action_tags, unidentified):
    """
    Tests whether ``is_single_source`` works as intended.
    
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
    output = is_single_source(characters, action_tags, unidentified)
    vampytest.assert_instance(output, bool)
    return output
