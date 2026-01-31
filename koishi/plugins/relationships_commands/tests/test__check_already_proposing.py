import vampytest
from hata import Component, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..checks import check_already_proposing


def _iter_options():
    user_id_0 = 202501030060
    user_id_1 = 202501030061
    user_id_2 = 202501030062
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    yield (
        None,
        user_1,
        0,
        None,
    )
    
    yield (
        [
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 500),
        ],
        user_1,
        0,
        None
    )
    
    yield (
        [
            RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500),
        ],
        user_1,
        0,
        [
            create_text_display(
                f'You have already sent an adoption agreement towards Koishi with 500 {EMOJI__HEART_CURRENCY}.\n'
                f'Cancel the old proposal before reissuing a new one.'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_already_proposing(source_relationship_request_listing, target_user, guild_id):
    """
    Tests whether ``check_already_proposing`` works as intended.
    
    Parameters
    ----------
    source_relationship_request_listing : `None | list<RelationshipRequest>`
        The relationship requests of the source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    output = check_already_proposing(source_relationship_request_listing, target_user, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
    
    return output
