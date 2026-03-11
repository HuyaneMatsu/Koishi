import vampytest
from hata import Component, User, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..component_building import build_relationship_request_accepted_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    user_id_0 = 202601170020
    user_id_1 = 202601170021
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    
    relationship_request = RelationshipRequest(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        False,
        relationship_request,
        user_1,
        0,
        2,
        [
            create_text_display(
                f'Koishi is now your mama.\n'
                f'Now you are daughter and mama.\n'
                f'You received half of their investment (500 {EMOJI__HEART_CURRENCY}).'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to requests',
                    custom_id = f'relationships_request.view.{user_id_0:x}.{False:x}.{2:x}',
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships_request.close.{user_id_0:x}',
                ),
            ),
        ],
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_relationship_request_accepted_components(
    user_id, outgoing, relationship_request, source_user, guild_id, page_index
):
    """
    Tests whether ``build_relationship_request_accepted_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The accepted relationship request.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_relationship_request_accepted_components(
        user_id, outgoing, relationship_request, source_user, guild_id, page_index
    )
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
