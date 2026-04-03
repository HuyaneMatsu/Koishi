import vampytest
from hata import (
    Component, Icon, IconType, User, create_button, create_row, create_section, create_separator,
    create_text_display, create_thumbnail_media
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU,
    RelationshipRequest
)

from ..component_building import build_relationship_request_listing_components
from ..constants import EMOJI_CLOSE, EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT


def _iter_options():
    guild_id = 202412310020
    
    user_id_0 = 202412310021
    user_id_1 = 202412310022
    user_id_2 = 202412310023
    user_id_3 = 202412310024
    user_id_4 = 202412310025
    user_id_5 = 202412310026
    
    user_0 = User.precreate(user_id_0, name = 'Satori', avatar = Icon(IconType.static, 2))
    user_1 = User.precreate(user_id_1, name = 'Utsuho')
    user_2 = User.precreate(user_id_2, name = 'Rin')
    user_3 = User.precreate(user_id_3, name = 'Koishi')
    user_4 = User.precreate(user_id_4, name = 'Kokoro')
    user_5 = User.precreate(user_id_5, name = 'Remilia')
    
    
    yield (
        user_0,
        True,
        None,
        None,
        0,
        0,
        0,
        [
            create_section(
                create_text_display(
                    '# Satori\'s outgoing requests\n'
                    '\n'
                    'Page: 1'
                ),
                thumbnail = create_thumbnail_media(
                    'https://cdn.discordapp.com/avatars/202412310021/00000000000000000000000000000002.png',
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = 'relationships_request.view.decrement.disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = 'relationships_request.view.increment.disabled',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships_request.close.{user_id_0:x}',
                ),
            ),
        ],
    )
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    entry_id_3 = 123
    entry_id_4 = 124
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000)
    relationship_request_0.entry_id = entry_id_0
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 2000)
    relationship_request_1.entry_id = entry_id_1
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 3000)
    relationship_request_2.entry_id = entry_id_2
    relationship_request_3 = RelationshipRequest(user_id_0, user_id_4, RELATIONSHIP_TYPE_MISTRESS, 4000)
    relationship_request_3.entry_id = entry_id_3
    relationship_request_4 = RelationshipRequest(user_id_0, user_id_5, RELATIONSHIP_TYPE_MISTRESS, 5000)
    relationship_request_4.entry_id = entry_id_4
    
    yield (
        user_0,
        True,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
            relationship_request_3,
            relationship_request_4,
        ],
        [
            user_1,
            user_2,
            user_3,
            user_4,
            user_5,
        ],
        0,
        1,
        2,
        [
            create_section(
                create_text_display(
                    '# Satori\'s outgoing requests\n'
                    '\n'
                    'Page: 2'
                ),
                thumbnail = create_thumbnail_media(
                    'https://cdn.discordapp.com/avatars/202412310021/00000000000000000000000000000002.png',
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'Adoption agreement towards Koishi (3000 {EMOJI__HEART_CURRENCY})'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'relationships_request.details.{user_id_0:x}.{True:x}.{1:x}.{entry_id_2:x}'
                ),
            ),
            create_section(
                create_text_display(
                    f'Employment contract towards Kokoro (4000 {EMOJI__HEART_CURRENCY})'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'relationships_request.details.{user_id_0:x}.{True:x}.{1:x}.{entry_id_3:x}'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = f'relationships_request.view.{user_id_0:x}.{True:x}.{0:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = f'relationships_request.view.{user_id_0:x}.{True:x}.{2:x}',
                    enabled = True,
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
def test__build_relationship_request_listing_components(
    user, outgoing, relationship_request_listing, users, guild_id, page_index, page_size
):
    """
    Tests whether ``build_relationship_request_listing_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request_listing : ``None | list<RelationshipRequest>``
        The relationship requests. They should not be chopped before calling this function.
    
    users : ``None | list<ClientUserBase>``
        The requested user for each relationship.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    page_size : `int`
        Page size to patch the builder with.
    
    Returns
    -------
    components : ``list<Component>``
    """
    mocked = vampytest.mock_globals(
        build_relationship_request_listing_components,
        PAGE_SIZE_DEFAULT = page_size,
    )
    output = mocked(
        user, outgoing, relationship_request_listing, users, guild_id, page_index
    )
    
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
