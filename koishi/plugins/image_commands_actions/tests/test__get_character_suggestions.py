import vampytest

from ...touhou_core import KAENBYOU_RIN, REIUJI_UTSUHO, YAKUMO_RAN

from ..action_filtering import PARAMETER_WILD_CARD, get_character_suggestions


def _iter_options():
    yield (
        [],
        False,
        None,
        None,
    )
    
    yield (
        [],
        True,
        None,
        [PARAMETER_WILD_CARD],
    )
    
    yield (
        [KAENBYOU_RIN, REIUJI_UTSUHO, YAKUMO_RAN],
        False,
        None,
        [PARAMETER_WILD_CARD, KAENBYOU_RIN.name, REIUJI_UTSUHO.name, YAKUMO_RAN.name],
    )
    
    yield (
        [],
        False,
        'ki',
        None,
    )
    
    yield (
        [KAENBYOU_RIN, REIUJI_UTSUHO, YAKUMO_RAN],
        False,
        'rin',
        ['rin', 'ran'],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_character_suggestions(parameters, allow_wild_card, input_value):
    """
    Tests whether ``get_character_suggestions`` works as intended.
    
    Parameters
    ----------
    characters : `set<TouhouCharacter>`
        Characters to auto complete from.
    allow_wild_card : `bool`
        Whether wild card option is allowed.
    input_value : `None`, `str`
        Characters to auto complete from.
    
    Returns
    -------
    output : `None | list<str>`
    """
    output = get_character_suggestions(parameters, allow_wild_card, input_value)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    return output
