__all__ = ()

import vampytest
from hata import (
    Component, Emoji, Guild, GuildProfile, Icon, IconType, Role, User, create_button, create_text_display, create_row,
    create_section, create_separator, create_thumbnail_media
)
from ...expression_tracking import ACTION_TYPE_EMOJI_CONTENT, ENTITY_FILTER_RULE_NONE

from ..component_building import build_components
from ..constants import EMOJI_CLOSE, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, MODE_GUILD_IN
from ..helpers import pack_action_types


def _iter_options():
    guild_id = 202512120021
    
    emoji_id_0 = 202512120022
    user_id = 202512120023
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = 'koishi',
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile()
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    guild = Guild.precreate(
        guild_id,
        name = 'Koishi',
        emojis = [emoji_0],
        roles = [role],
        users = [user],
        icon = Icon(IconType.static, 2),
    )
    
    action_types_packed = pack_action_types((ACTION_TYPE_EMOJI_CONTENT, ))
    
    yield (
        user,
        user,
        guild,
        [
            (emoji_id_0, 5),
        ],
        1,
        MODE_GUILD_IN,
        action_types_packed,
        ENTITY_FILTER_RULE_NONE,
        12,
        1,
        20,
        True,
        [
            create_section(
                create_text_display(
                    '# In Koishi\'s emojis in content\n'
                    'Page: 2; page size: 20; months: 12; order: decreasing'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/icons/{guild_id!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_text_display(
                f'`Total |   Source | Emojis`\n'
                f'`    5 | internal | ` {emoji_0.as_emoji}'
            ),
            create_separator(),
            create_row(
                create_button(
                    f'Page {1!s}',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = (
                        f'expression_tracking.stats.{user_id:x}.{MODE_GUILD_IN:x}.{guild_id:x}.{action_types_packed:x}.'
                        f'{0:x}.{12:x}.{0:x}.{20:x}.{True:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    f'Page {3!s}',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'expression_tracking.disabled.1',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'expression_tracking.close.{user_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_components(
    client,
    user,
    guild,
    entries,
    page_count,
    mode,
    action_types_packed,
    entity_filter_rule,
    months,
    page_index,
    page_size,
    order_decreasing,
):
    """
    Tests whether ``build_components`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    user : ``ClientUserBase``
        The user invoking this interaction.
    
    guild : ``None | Guild``
        The guild in context.
    
    entries : `list<tuple<int>>`
        Entries to render.
    
    page_count : `int`
        The amount of pages.
    
    mode : `int`
        The usage mode to respond with.
    
    action_types_packed : `int`
        The action types packed.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to look back.
    
    page_index : `int`
        The page's index to display.
    
    page_size : `int`
        The page's size to display.
    
    order_decreasing : `bool`
        Whether to order in a decreasing order.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_components(
        client,
        user,
        guild,
        entries,
        page_count,
        mode,
        action_types_packed,
        entity_filter_rule,
        months,
        page_index,
        page_size,
        order_decreasing,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
