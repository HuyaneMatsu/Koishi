import vampytest
from hata import (
    ApplicationCommandOptionType, InteractionEvent, InteractionMetadataApplicationCommandAutocomplete,
    InteractionOption, InteractionType
)

from ...touhou_core import KAENBYOU_RIN, REIUJI_UTSUHO

from ..action_filtering import (
    ACTION_NAME_TO_TAG, PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET, PARAMETER_WILD_CARD,
    autocomplete_action_tag
)


def _iter_options():
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_ACTION_TAG,
                        value = None,
                    ),
                ],
            )
        ),
        None,
        [PARAMETER_WILD_CARD, *sorted(ACTION_NAME_TO_TAG.keys())],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_ACTION_TAG,
                        value = 'f',
                    ),
                ],
            )
        ),
        'f',
        ['feed', 'fluff'],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_ACTION_TAG,
                        value = None,
                    ),
                    InteractionOption(
                        focused = False,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_SOURCE,
                        value = KAENBYOU_RIN.name,
                    ),
                    InteractionOption(
                        focused = False,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_TARGET,
                        value = REIUJI_UTSUHO.name,
                    ),
                ],
            )
        ),
        None,
        [PARAMETER_WILD_CARD, 'hug'],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_ACTION_TAG,
                        value = 'h',
                    ),
                    InteractionOption(
                        focused = False,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_SOURCE,
                        value = KAENBYOU_RIN.name,
                    ),
                    InteractionOption(
                        focused = False,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_TARGET,
                        value = REIUJI_UTSUHO.name,
                    ),
                ],
            )
        ),
        'h',
        ['hug'],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__autocomplete_action_tag(event, input_value):
    """
    Tests whether ``autocomplete_action_tag`` works as intended.
    
    This function is a coroutine.
    
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
    output = await autocomplete_action_tag(event, input_value)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    return output
