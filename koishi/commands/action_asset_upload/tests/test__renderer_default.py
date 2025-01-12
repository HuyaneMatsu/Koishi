import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN

from ..rendering import renderer_default


def _iter_options():
    yield (
        None,
        None,
        None,
        None,
        'https://orindance.party/miau',
        (
            '# TODO\n'
            'TOUHOU_ACTION_ALL.add(\n'
            '    \'https://orindance.party/miau\',\n'
            ')\n'
            '\n'
        ),
    )
    
    yield (
        {CHEN, YAKUMO_RAN},
        {'hug', 'kiss'},
        {'hey', 'mister'},
        'sister',
        'https://orindance.party/miau',
        (
            '# TODO hey mister\n'
            'TOUHOU_ACTION_ALL.add(\n'
            '    \'https://orindance.party/miau\',\n'
            ').with_actions(\n'
            '    (ACTION_TAG_HUG, None, None),\n'
            '    (ACTION_TAG_KISS, None, None),\n'
            ').with_characters(\n'
            '    CHEN,\n'
            '    YAKUMO_RAN,\n'
            ').with_creator(\n'
            '    \'sister\',\n'
            ')\n'
            '\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__renderer_default(characters, action_tags, unidentified, creator, url):
    """
    Tests whether ``renderer_default`` works as intended.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    creator : `None | str`
        The image's creator.
    
    url : `str`
        Url to the image.
    
    Returns
    -------
    output : `str`
    """
    output = renderer_default(characters, action_tags, unidentified, creator, url)
    vampytest.assert_instance(output, str)
    return output
