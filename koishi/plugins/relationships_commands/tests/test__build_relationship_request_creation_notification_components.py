import vampytest
from hata import ButtonStyle, Component, User, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_WAIFU, RelationshipRequest

from ..component_building import build_relationship_request_creation_notification_components


def _iter_options():
    user_id_0 = 202601180000
    user_id_1 = 202601180001
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    
    entry_id_0 = 120
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000)
    relationship_request_0.entry_id = entry_id_0
    
    yield (
        user_0,
        relationship_request_0,
        user_id_1,
        0,
        [
            create_text_display(
                f'Satori wants to marry you.\n'
                f'They are proposing with 1000 {EMOJI__HEART_CURRENCY}.',
            ),
            create_separator(),
            create_row(
                create_button(
                    'Accept',
                    custom_id = f'relationships_request.accept.{user_id_1:x}.{False:x}.{0:x}.{entry_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Reject',
                    custom_id = f'relationships_request.reject.{user_id_1:x}.{False:x}.{0:x}.{entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.notification_proposal.disable',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_relationship_request_creation_notification_components(
    source_user, relationship_request, target_user_id, guild_id
):
    """
    Tests whether ``build_relationship_request_creation_notification_components`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who created the relationship request.
    
    relationship_request : ``RelationshipRequest``
        The relationship requests to display.
    
    target_user_id : `int`
        The targeted user's identifier.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_relationship_request_creation_notification_components(
        source_user, relationship_request, target_user_id, guild_id
    )
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
