from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Component, Icon, IconType, StringSelectOption, User, create_button, create_row, create_section, create_separator,
    create_string_select, create_text_display, create_thumbnail_media
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU, Relationship,
    RelationshipExtensionTrace, RelationshipRequest
)
from ...user_balance import UserBalance

from ..component_building import build_relationship_listing_components
from ..constants import EMOJI_CLOSE, EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT, RELATIONSHIP_LISTING_MODE_LEGACY


def _iter_options():
    user_id_00 = 202601250000
    user_id_01 = 202601250001
    user_id_02 = 202601250002
    user_id_03 = 202601250003
    user_id_04 = 202601250004
    user_id_05 = 202601250005
    user_id_06 = 202601250006
    
    user_00 = User.precreate(
        user_id_00,
        avatar = Icon(IconType.static, 4),
        name = 'Satori',
    )
    
    user_01 = User.precreate(
        user_id_01,
        name = 'Koishi',
    )
    
    user_02 = User.precreate(
        user_id_02,
        name = 'Remilia',
    )
    
    user_03 = User.precreate(
        user_id_03,
        name = 'Flandre',
    )
    
    user_04 = User.precreate(
        user_id_04,
        name = 'Patchouli',
    )
    
    user_05 = User.precreate(
        user_id_05,
        name = 'Koakuma',
    )
    
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    # self-target & empty
    
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    yield (
        'self-target + empty + page 2',
        user_00,
        user_00,
        None,
        0,
        user_balance_00,
        None,
        None,
        RELATIONSHIP_LISTING_MODE_LEGACY,
        1,
        [
            create_section(
                create_text_display(
                    '# Satori\'s relationship info\n'
                    '\n'
                    'Listing mode: legacy; Page: 2\n'
                    'Value: 550 - 1050; Break-ups: 0; Slots: 0 / 1'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000004.png',
                ),
            ),
            create_separator(),
            create_row(
                create_string_select(
                    [
                        StringSelectOption(
                            '0',
                            'Legacy',
                            default = True,
                        ),
                        StringSelectOption(
                            '1',
                            'Long',
                            default = False,
                        ),
                        StringSelectOption(
                            '2',
                            'Wide',
                            default = False
                        ),
                    ],
                    f'relationships.mode.{user_id_00:x}.{user_id_00:x}.{1:x}'
                )
            ),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = f'relationships.view.{user_id_00:x}.{user_id_00:x}.{0:x}.{0:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = 'relationships.view.increment.disabled',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships.close.{user_id_00:x}'
                ),
            ),
        ],
    )
    
    # other target + value + relationships + indirect relationships + relationship requests
    user_balance_01 = UserBalance(user_id_01)
    user_balance_01.relationship_divorces = 4
    user_balance_01.relationship_slots = 9
    user_balance_01.relationship_value = 9999
    
    relationship_00 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_01 = Relationship(user_id_01, user_id_03, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_02 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_03 = Relationship(user_id_02, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    relationship_request_00 = RelationshipRequest(user_id_00, user_id_06, RELATIONSHIP_TYPE_SISTER_BIG, 1200)
    
    yield (
        'other target + value + relationships + indirect relationships + relationship requests',
        user_00,
        user_01,
        [
            user_02,
            user_03,
            user_04,
            user_05,
        ],
        0,
        user_balance_01,
        {
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_01,),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_02,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_00, relationship_03,),
            ),
        },
        [
            relationship_request_00,
        ],
        RELATIONSHIP_LISTING_MODE_LEGACY,
        0,
        [
            create_section(
                create_text_display(
                    '# Koishi\'s relationship info\n'
                    '\n'
                    'Listing mode: legacy; Page: 1\n'
                    'Value: 11430 - 21821; Break-ups: 4; Slots: 4 (3 + 1) / 9'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/embed/avatars/3.png',
                ),
            ),
            create_separator(),
            create_text_display(
                '### Waifu\n'
                '- Remilia\n'
                '### Big sister\n'
                '- Patchouli\n'
                '### Lil sisters\n'
                '- Flandre\n'
                '- Koakuma (in law)'
            ),
            create_separator(),
            create_text_display(
                f'To propose to Koishi you need at least 21821 {EMOJI__HEART_CURRENCY}.'
            ),
            create_separator(),
            create_row(
                create_string_select(
                    [
                        StringSelectOption(
                            '0',
                            'Legacy',
                            default = True,
                        ),
                        StringSelectOption(
                            '1',
                            'Long',
                            default = False,
                        ),
                        StringSelectOption(
                            '2',
                            'Wide',
                            default = False
                        ),
                    ],
                    f'relationships.mode.{user_id_00:x}.{user_id_01:x}.{0:x}'
                )
            ),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = 'relationships.view.decrement.disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = 'relationships.view.increment.disabled',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'relationships.close.{user_id_00:x}'
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test_build_relationship_listing_components(
    source_user,
    target_user,
    users,
    guild_id,
    target_user_balance,
    target_relationship_extension_traces,
    target_relationship_request_listing,
    relationship_listing_mode,
    page_index,
):
    """
    Tests whether ``build_relationship_listing_components`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is listing the relationships.
    
    target_user : ``ClientUserBase``
        The user who's relationships are being listed.
    
    users : ``None | list<ClientUserBase>``
        The user entities the `target_user` has relationships with.
    
    guild_id : `int`
        The respective guild's identifier.
    
    target_user_balance : ``UserBalance``
        The targeted user's user balance.
    
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
        Relationship extension traces to display.
    
    target_relationship_request_listing : `None | list<RelationshipProposal>`
        The outgoing relationship proposals of the targeted user.
    
    relationship_listing_mode : `int`
        The mode to render as.
    
    page_index : `int`
        The page's index to display.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_relationship_listing_components(
        source_user,
        target_user,
        users,
        guild_id,
        target_user_balance,
        target_relationship_extension_traces,
        target_relationship_request_listing,
        relationship_listing_mode,
        page_index,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
