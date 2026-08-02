import vampytest
from hata import (
    Guild, InteractionForm, StringSelectOption, TextInputStyle, User, create_label, create_string_select,
    create_text_input, create_user_select
)

from ..component_building import build_mod_other_form
from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_INVITES_DISABLE, ACTION_TYPE_MUTE, DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
    REASON_ALLOWED_LENGTH_THRESHOLD
)


def _iter_options():
    guild = Guild.precreate(202607160011, name = 'Moriya shrine')
    user = User.precreate(202607160040, name = 'Suwako')
    
    yield (
        ACTION_TYPE_BAN,
        None,
        guild,
        None,
        3600,
        3600,
        InteractionForm(
            f'Banning user(s) from Moriya shrine.',
            [
                create_label(
                    'Select users',
                    None,
                    create_user_select(
                        custom_id = 'users',
                        min_values = 1,
                        required = True,
                    ),
                ),
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
                    'Notify user',
                    None,
                    create_string_select(
                        [
                            StringSelectOption('0', 'Nah', default = True),
                            StringSelectOption('1', 'Yes'),
                        ],
                        custom_id = 'notify_user',
                    ),
                ),
                create_label(
                    'Delete message duration',
                    'w for week, d for day, h for hour, m for minute, s for second.',
                    create_text_input(
                        custom_id = 'delete_message_duration',
                        max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
                        value = '1h',
                    ),
                ),
            ],
            custom_id =  f'mod.other.{ACTION_TYPE_BAN:x}.{0:x}',
        ),
    )
    
    yield (
        ACTION_TYPE_BAN,
        user,
        guild,
        'frog',
        7200,
        3600,
        InteractionForm(
            f'Banning Suwako from Moriya shrine.',
            [
                create_label(
                    'Reason',
                    None,
                    create_text_input(
                        custom_id = 'reason',
                        max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                        value = 'frog',
                        style = TextInputStyle.paragraph,
                    ),
                ),
                create_label(
                    'Notify user',
                    None,
                    create_string_select(
                        [
                            StringSelectOption('0', 'Nah', default = True),
                            StringSelectOption('1', 'Yes'),
                        ],
                        custom_id = 'notify_user',
                    ),
                ),
                create_label(
                    'Delete message duration',
                    'w for week, d for day, h for hour, m for minute, s for second.',
                    create_text_input(
                        custom_id = 'delete_message_duration',
                        max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
                        value = '2h',
                    ),
                ),
            ],
            custom_id =  f'mod.other.{ACTION_TYPE_BAN:x}.{user.id:x}',
        ),
    )
    
    yield (
        ACTION_TYPE_MUTE,
        user,
        guild,
        'frog',
        3600,
        7200,
        InteractionForm(
            f'Muting Suwako in Moriya shrine.',
            [
                create_label(
                    'Reason',
                    None,
                    create_text_input(
                        custom_id = 'reason',
                        max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                        value = 'frog',
                        style = TextInputStyle.paragraph,
                    ),
                ),
                create_label(
                    'Notify user',
                    None,
                    create_string_select(
                        [
                            StringSelectOption('0', 'Nah', default = True),
                            StringSelectOption('1', 'Yes'),
                        ],
                        custom_id = 'notify_user',
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
            custom_id =  f'mod.other.{ACTION_TYPE_MUTE:x}.{user.id:x}',
        ),
    )
    
    yield (
        ACTION_TYPE_INVITES_DISABLE,
        None,
        guild,
        'frog',
        3600,
        7200,
        InteractionForm(
            f'Disabling invites of Moriya shrine.',
            [
                create_label(
                    'Reason',
                    None,
                    create_text_input(
                        custom_id = 'reason',
                        max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                        value = 'frog',
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            custom_id =  f'mod.other.{ACTION_TYPE_INVITES_DISABLE:x}.{0:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_other_form(
    action_type, target, guild, reason_default, delete_message_days_duration_default, duration_default
):
    """
    Tests whether ``build_mod_other_form`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    target : ``None | ClientUserBase``
        The targeted user if any.
    
    guild : ``Guild``
        The local guild.
    
    reason_default : `None | str`
        Default reason to use.
    
    delete_message_days_duration_default : `int`
        Default delete message days duration.
    
    duration_default : `int`
        Default duration.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_mod_other_form(
        action_type, target, guild, reason_default, delete_message_days_duration_default, duration_default
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
