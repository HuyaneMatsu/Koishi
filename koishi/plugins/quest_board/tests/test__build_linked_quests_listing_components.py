import vampytest

from hata import (
    BUILTIN_EMOJIS, CDN_ENDPOINT, Component, GuildProfile, Icon, IconType, User, create_button, create_row,
    create_section, create_separator, create_text_display, create_thumbnail_media
)

from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, get_quest_template
)
from ...user_stats_core import UserStats

from ..component_building import build_linked_quests_listing_components
from ..constants import EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS


def _iter_options():
    user_id = 202505240010
    user_name = 'Nue'
    guild_id = 202505240011
    user_nick = 'You must be new here'
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        5666,
        Quest(
            quest_template_id_0,
            quest_amount_0,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        57777,
        Quest(
            quest_template_id_1,
            quest_amount_1,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_entry_id_1 = 124
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    
    yield (
        user_id,
        user_name,
        Icon(IconType.static, 2),
        guild_id,
        user_nick,
        Icon(IconType.static, 3),
        1 << 7,
        [
            linked_quest_0,
            linked_quest_1,
        ],
        0,
        [
            create_section(
                create_text_display(
                    f'# {user_nick}\'s quests\n'
                    f'\n'
                    f'User rank: D\n'
                    f'Quest count: 2 / 3'
                ),
                thumbnail = create_thumbnail_media(
                    f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000003.png',
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'Time left: 59 minutes, 59 seconds\n'
                    f'Submit 0 / {quest_amount_0} Carrot {BUILTIN_EMOJIS["carrot"]} to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'linked_quest.details.{linked_quest_entry_id_0:x}',
                ),
            ),
            create_section(
                create_text_display(
                    f'Time left: 59 minutes, 59 seconds\n'
                    f'Submit 0 / {quest_amount_1} Peach {BUILTIN_EMOJIS["peach"]} to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'linked_quest.details.{linked_quest_entry_id_1:x}',
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    emoji = EMOJI_PAGE_PREVIOUS,
                    custom_id = 'linked_quest.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    emoji = EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.page_increment_disabled',
                    enabled = False,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quests_listing_components(
    user_id,
    user_name,
    user_avatar,
    guild_id,
    user_nick,
    user_guild_avatar,
    credibility,
    linked_quest_listing,
    page_index,
):
    """
    Tests whether ``build_linked_quests_listing_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    user_name : `int`
        The user's name.
    
    user_avatar : ``None | Icon``
        The user's avatar.
    
    guild_id : `int`
        The respective guild's identifier the command was invoked at.
    
    user_nick : `int`
        The user's nick name.
    
    user_guild_avatar : ``None | Icon``
        The user's avatar in the guild.
    
    credibility : `int`
        The guild's  credibility.
    
    linked_quest_listing : ``None | list<LinkedQuest>``
        The user's accepted quests.
    
    page_index : `int`
        The page's index to show.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user = User.precreate(user_id, avatar = user_avatar, name = user_name)
    
    if guild_id and ((user_nick is not None) or (user_guild_avatar is not None)):
        user.guild_profiles[guild_id] = GuildProfile(avatar = user_guild_avatar, nick = user_nick)
    
    user_stats = UserStats(user_id)
    user_stats.set('credibility', credibility)
    
    
    output = build_linked_quests_listing_components(user, guild_id, user_stats, linked_quest_listing, page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
