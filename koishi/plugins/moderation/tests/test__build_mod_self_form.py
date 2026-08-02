import vampytest
from hata import Guild, InteractionForm, TextInputStyle, create_label, create_text_input

from ..component_building import build_mod_self_form
from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_MUTE, DURATION_ALLOWED_LENGTH_MAX_THRESHOLD, REASON_ALLOWED_LENGTH_THRESHOLD
)


def _iter_options():
    guild = Guild.precreate(202607160015, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        guild,
        3600,
        InteractionForm(
            f'Banning yourself from Moriya shrine.',
            [
                create_label(
                    'Reason',
                    None,
                    create_text_input(
                        custom_id = 'reason',
                        max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                        value = None,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            custom_id =  f'mod.self.{ACTION_TYPE_BAN:x}',
        ),
    )
    
    yield (
        ACTION_TYPE_MUTE,
        guild,
        7200,
        InteractionForm(
            f'Muting yourself in Moriya shrine.',
            [
                create_label(
                    'Reason',
                    None,
                    create_text_input(
                        custom_id = 'reason',
                        max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                        value = None,
                        style = TextInputStyle.paragraph,
                    ),
                ),
                create_label(
                    'Duration',
                    'w for week, d for day, h for hour, m for minute, s for second.',
                    create_text_input(
                        custom_id = 'duration',
                        max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
                        value = '2h',
                    ),
                ),
            ],
            custom_id =  f'mod.self.{ACTION_TYPE_MUTE:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_self_form(
    action_type, guild, duration_default
):
    """
    Tests whether ``build_mod_self_form`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    duration_default : `int`
        Default duration.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_mod_self_form(
        action_type, guild, duration_default
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
