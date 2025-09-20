import vampytest
from hata import ApplicationCommandOptionType, InteractionEvent, InteractionOption, InteractionType

from ...touhou_core import KAENBYOU_RIN, KOMEIJI_KOISHI, NAZRIN, REIUJI_UTSUHO

from ..action_filtering import (
    PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET, PARAMETER_WILD_CARD, get_target_character_suggestions
)


def _iter_options():
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            options = [
                InteractionOption(
                    focused = True,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_TARGET,
                    value = None,
                ),
            ],
        ),
        None,
        [PARAMETER_WILD_CARD, 'Aki Minoriko', 'Aki Shizuha', 'Chen', 'Chiruno'],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            options = [
                InteractionOption(
                    focused = True,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_TARGET,
                    value = None,
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_ACTION_TAG,
                    value = 'hug',
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_SOURCE,
                    value = KAENBYOU_RIN.name,
                ),
            ],
        ),
        None,
        [PARAMETER_WILD_CARD, KAENBYOU_RIN.name, NAZRIN.name, REIUJI_UTSUHO.name],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            options = [
                InteractionOption(
                    focused = True,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_TARGET,
                    value = 'ran',
                ),
            ],
        ),
        'ran',
        ['ran', 'seiran', 'rin'],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            options = [
                InteractionOption(
                    focused = True,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_TARGET,
                    value = 'rei',
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_ACTION_TAG,
                    value = 'hug',
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_SOURCE,
                    value = KAENBYOU_RIN.name,
                ),
            ],
        ),
        'rei',
        ['reiuji utsuho', 'rin'],
    )
    
    # Allow duplication only if source == target
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            options = [
                InteractionOption(
                    focused = True,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_TARGET,
                    value = 'koi',
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_ACTION_TAG,
                    value = 'hug',
                ),
                InteractionOption(
                    focused = False,
                    option_type = ApplicationCommandOptionType.string,
                    name = PARAMETER_NAME_SOURCE,
                    value = KOMEIJI_KOISHI.name,
                ),
            ],
        ),
        'koi',
        ['koishi'],
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_target_character_suggestions(event, input_value):
    """
    Tests whether ``get_target_character_suggestions`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    input_value : `None`, `str`
        The value to autocomplete.
    
    Returns
    -------
    output : `None | list<str>`
    """
    output = get_target_character_suggestions(event, input_value)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    del output[5:]
    return output
