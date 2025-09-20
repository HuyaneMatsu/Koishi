import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN

from ..rendering import producer_cross_target


def _iter_options():
    yield (
        CHEN,
        YAKUMO_RAN,
        'handhold',
        'sister',
        'https://orindance.party/miau',
        (
            'TOUHOU_ACTION_ALL.add(\n'
            '    \'https://orindance.party/miau\',\n'
            ').with_actions(\n'
            '    (ACTION_TAG_HANDHOLD, CHEN, YAKUMO_RAN),\n'
            '    (ACTION_TAG_HANDHOLD, YAKUMO_RAN, CHEN),\n'
            ').with_creator(\n'
            '    \'sister\',\n'
            ')\n'
            '\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__producer_cross_target(source_character_0, source_character_1, action_tag, creator, url):
    """
    Tests whether ``producer_cross_target`` works as intended.
    
    Parameters
    ----------
    source_character_0 : ``TouhouCharacter``
        Source character.
    
    source_character_1 : ``TouhouCharacter``
        Source character.
    
    action_tag : `str`
        Action tag.
    
    creator : `None | str`
        The image's creator.
    
    Returns
    -------
    output : `str`
    """
    output = [*producer_cross_target({source_character_0, source_character_1}, {action_tag}, None, creator, url)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
