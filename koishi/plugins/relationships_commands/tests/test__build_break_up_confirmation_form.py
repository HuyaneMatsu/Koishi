import vampytest
from hata import InteractionForm, User, create_text_display

from ..component_building import build_break_up_confirmation_form


def _iter_options():
    user_id = 202601130000
    user = User.precreate(
        user_id,
        name = 'Satori',
    )
    
    yield (
        user,
        0,
        InteractionForm(
            'Break up confirmation',
            [
                create_text_display(
                    'Are you sure to break up with Satori?'
                ),
            ],
            custom_id = f'relationships.break_up.{user_id:x}',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_break_up_confirmation_form(target_user, guild_id):
    """
    Tests whether ``build_break_up_confirmation_form`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to be broke up with.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    --------
    output : ``InteractionForm``
    """
    output = build_break_up_confirmation_form(target_user, guild_id)
    vampytest.assert_instance(output, InteractionForm)
    return output
