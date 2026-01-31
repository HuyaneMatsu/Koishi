import vampytest
from hata import Component, User, create_text_display

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..component_building import build_update_unset_success_components


def _iter_options():
    target_user = User.precreate(
        202501090001,
        name = 'Satori',
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        target_user,
        0,
        [
            create_text_display('You have become the mama of Satori.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_update_unset_success_components(relationship_type, target_user, guild_id):
    """
    Tests whether ``build_update_unset_success_components`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    target_user : ``ClientUserBase``
        The targeted user. May be actually the source user if the relationship is reversed.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_update_unset_success_components(relationship_type, target_user, guild_id)
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
