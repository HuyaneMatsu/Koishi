import vampytest
from hata import Component, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..component_building import build_request_created_success_components


def _iter_options():
    target_user = User.precreate(
        202412290005,
        name = 'Satori',
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        [
            create_text_display(
                f'You sent an adoption agreement to Satori '
                f'with 1000 {EMOJI__HEART_CURRENCY}'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_request_created_success_components(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``build_request_created_success_components`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_request_created_success_components(relationship_type, investment, target_user, guild_id)
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
