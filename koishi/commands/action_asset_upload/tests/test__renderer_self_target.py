import vampytest

from ....plugins.touhou_core import CHEN

from ..rendering import renderer_self_target


def _iter_options():
    yield (
        CHEN,
        'feed_self',
        'sister',
        'https://orindance.party/miau',
        (
            'TOUHOU_ACTION_ALL.add(\n'
            '    \'https://orindance.party/miau\',\n'
            ').with_action(\n'
            '    ACTION_TAG_FEED_SELF, CHEN, CHEN,\n'
            ').with_creator(\n'
            '    \'sister\',\n'
            ')\n'
            '\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__renderer_self_target(source_character, action_tag, creator, url):
    """
    Tests whether ``renderer_self_target`` works as intended.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        Source character.
    
    action_tag : `str`
        Action tag.
    
    creator : `None | str`
        The image's creator.
    
    Returns
    -------
    output : `str`
    """
    output = renderer_self_target({source_character}, {action_tag}, None, creator, url)
    vampytest.assert_instance(output, str)
    return output
