import vampytest
from hata import (
    ApplicationCommandOptionType, InteractionEvent, InteractionMetadataApplicationCommandAutocomplete,
    InteractionOption, InteractionType
)

from ...touhou_core import KAENBYOU_RIN, REIUJI_UTSUHO

from ..action_filtering import (
    PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_NAME, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET, PARAMETER_WILD_CARD,
    autocomplete_name
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
                        name = PARAMETER_NAME_NAME,
                        value = None,
                    ),
                ],
            )
        ),
        None,
        [
            PARAMETER_WILD_CARD, 'akyuu-kosuzu-pocky-0000', 'alice-marisa-kiss-0000', 'alice-marisa-kiss-0001',
            'alice-marisa-lick-0000',
        ],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_NAME,
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
        [PARAMETER_WILD_CARD, 'okuu-orin-hug-0002', 'okuu-orin-hug-0005', 'okuu-orin-hug-0007'],
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_NAME,
                        value = 'ran',
                    ),
                ],
            )
        ),
        'ran',
        ['ran-fluffy-tail-0000', 'ran-kon-0000', 'ran-kon-0001', 'ran-kon-0002', 'ran-kon-0003'],
    )
    
    yield (
        InteractionEvent(
            interaction_type = InteractionType.application_command_autocomplete,
            interaction = InteractionMetadataApplicationCommandAutocomplete(
                options = [
                    InteractionOption(
                        focused = True,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_NAME,
                        value = 'ok',
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
                    InteractionOption(
                        focused = False,
                        option_type = ApplicationCommandOptionType.string,
                        name = PARAMETER_NAME_TARGET,
                        value = REIUJI_UTSUHO.name,
                    ),
                ],
            )
        ),
        'okuu-orin-hug-0002',
        ['okuu-orin-hug-0002'],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__autocomplete_name(event, input_value):
    """
    Tests whether ``autocomplete_name`` works as intended.
    
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
    output = await autocomplete_name(event, input_value)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    del output[5:]
    return output
