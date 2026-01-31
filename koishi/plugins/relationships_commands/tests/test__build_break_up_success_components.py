import vampytest
from hata import Component, User, create_button, create_row, create_text_display

from ..component_building import build_break_up_success_components


def _iter_options():
    target_user = User.precreate(
        202601130001,
        name = 'Satori',
    )
    
    yield (
        target_user,
        0,
        0,
        0,
        [
            create_text_display(
                'You have broke up with Satori.'
            ),
            create_row(
                create_button(
                    'Burn the divorce papers!',
                    custom_id = f'user.burn_divorce_papers.invoke.{0:x}',
                )
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_break_up_success_components(target_user, source_received, target_received, guild_id):
    """
    tests whether ``build_break_up_success_components`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    source_received : `int`
        The amount of balance the source user received.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    output = build_break_up_success_components(target_user, source_received, target_received, guild_id)
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
