import vampytest
from hata import ButtonStyle, Component, User, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_WAIFU, RelationshipRequest

from ..component_building import build_relationship_request_details_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    user_id_0 = 202601170000
    user_id_1 = 202601170001
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    
    entry_id_0 = 120
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000)
    relationship_request_0.entry_id = entry_id_0
    
    yield (
        user_0,
        True,
        relationship_request_0,
        user_1,
        0,
        2,
        [
            create_text_display(
                f'Marriage proposal towards Koishi (1000 {EMOJI__HEART_CURRENCY})',
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to requests',
                    custom_id = f'relationships_request.view.{user_id_0:x}.{True:x}.{2:x}',
                ),
                create_button(
                    'Cancel',
                    custom_id = f'relationships_request.cancel.{user_id_0:x}.{True:x}.{2:x}.{entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships_request.close.{user_id_0:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_1,
        False,
        relationship_request_0,
        user_0,
        0,
        2,
        [
            create_text_display(
                f'Marriage proposal from Satori (1000 {EMOJI__HEART_CURRENCY})',
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to requests',
                    custom_id = f'relationships_request.view.{user_id_1:x}.{False:x}.{2:x}',
                ),
                create_button(
                    'Accept',
                    custom_id = f'relationships_request.accept.{user_id_1:x}.{False:x}.{2:x}.{entry_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Reject',
                    custom_id = f'relationships_request.reject.{user_id_1:x}.{False:x}.{2:x}.{entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships_request.close.{user_id_1:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_relationship_request_details_components(
    user, outgoing, relationship_request, target_user, guild_id, page_index
):
    """
    Tests whether ``build_relationship_request_details_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The relationship requests to display.
    
    target_user : ``ClientUserBase``
        The other user of the relationship request.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_relationship_request_details_components(
        user, outgoing, relationship_request, target_user, guild_id, page_index
    )
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
