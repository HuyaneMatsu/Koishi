from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import (
    BUILTIN_EMOJIS, ButtonStyle, CDN_ENDPOINT, Component, GuildProfile, Icon, IconType, User, create_button,
    create_row, create_section, create_separator, create_text_display, create_thumbnail_media
)

from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, get_quest_template
)
from ...user_stats_core import UserStats

from ..component_building import build_linked_quests_listing_components
from ..constants import EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS


class DateTimeMock(DateTime):
    __slots__ = ()
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, tz):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(tz)
        return value


def _iter_options():
    user_id = 202505240010
    user_name = 'Nue'
    guild_id_0 = 202505240011
    guild_id_1 = 202510130010
    user_nick = 'You must be new here'
    quest_duration = 3600
    now = DateTime(2016, 5, 14, 0, 0, 20, tzinfo = TimeZone.utc)
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 3600
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    
    
    quest_0 = Quest(
        quest_template_id_0,
        quest_amount_0,
        quest_duration,
        2,
        1000,
    )
    
    quest_1 = Quest(
        quest_template_id_1,
        quest_amount_1,
        quest_duration,
        2,
        1000,
    )
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id_0,
        5666,
        quest_0,
    )
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    linked_quest_0.taken_at = now - TimeDelta(seconds = 20)
    linked_quest_0.expires_at = now + TimeDelta(seconds = quest_duration - 20)
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id_0,
        57777,
        quest_1,
    )
    linked_quest_entry_id_1 = 124
    linked_quest_1.entry_id = linked_quest_entry_id_1
    linked_quest_1.taken_at = now - TimeDelta(seconds = 20)
    linked_quest_1.expires_at = now + TimeDelta(seconds = quest_duration - 20)
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id_1,
        57774,
        Quest(
            quest_template_id_1,
            quest_amount_1,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_entry_id_2 = 124
    linked_quest_2.entry_id = linked_quest_entry_id_2
    linked_quest_2.completion_count = 1
    linked_quest_2.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    linked_quest_3 = LinkedQuest(
        user_id,
        guild_id_0,
        57775,
        Quest(
            quest_template_id_1,
            quest_amount_1,
            3600,
            3,
            1000,
        ),
    )
    linked_quest_entry_id_3 = 135
    linked_quest_3.entry_id = linked_quest_entry_id_3
    linked_quest_3.completion_count = 3
    linked_quest_3.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    linked_quest_4 = LinkedQuest(
        user_id,
        guild_id_0,
        57125,
        Quest(
            quest_template_id_1,
            quest_amount_1,
            3600,
            3,
            1000,
        ),
    )
    linked_quest_entry_id_4 = 149
    linked_quest_4.entry_id = linked_quest_entry_id_4
    linked_quest_4.taken_at = now - TimeDelta(seconds = 20)
    linked_quest_4.expires_at = now
    
    page_index = 0
    
    yield (
        user_id,
        user_name,
        Icon(IconType.static, 2),
        guild_id_0,
        user_nick,
        Icon(IconType.static, 3),
        1 << 11,
        [
            linked_quest_3,
            linked_quest_2,
            linked_quest_0,
            linked_quest_1,
            linked_quest_4,
        ],
        page_index,
        now,
        [
            create_section(
                create_text_display(
                    f'# {user_nick}\'s quests\n'
                    f'\n'
                    f'User rank: D\n'
                    f'Active quest count: 3 / 3'
                ),
                thumbnail = create_thumbnail_media(
                    f'{CDN_ENDPOINT}/guilds/{guild_id_0}/users/{user_id}/avatars/00000000000000000000000000000003.png',
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'Time left: 59 minutes, 40 seconds\n'
                    f'Submit 0.00 / {quest_amount_0/1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'linked_quest.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_section(
                create_text_display(
                    f'Time left: 59 minutes, 40 seconds\n'
                    f'Submit 0 / {quest_amount_1} {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'linked_quest.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id_1:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_section(
                create_text_display(
                    f'Expired\n'
                    f'Submit 0 / {quest_amount_1} {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'linked_quest.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id_4:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.red,
                ),
            ),
            create_section(
                create_text_display(
                    f'Completed: 1 / 3 times, re-acceptable for 23 hours, 59 minutes, 40 seconds\n'
                    f'Submit {quest_amount_1} {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'quest_board.details.{user_id:x}.{guild_id_1:x}.{0:x}.{quest_template_id_1:x}',
                    enabled = True,
                    style = ButtonStyle.blue,
                ),
            ),
            create_section(
                create_text_display(
                    f'Completed: 3 / 3 times, cannot be re-accepted anymore\n'
                    f'Submit {quest_amount_1} {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'quest_board.details.{user_id:x}.{guild_id_0:x}.{0:x}.{quest_template_id_1:x}',
                    enabled = True,
                    style = ButtonStyle.gray,
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
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{0:x}',
                    enabled = True,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quests_listing_components(
    user_id,
    user_name,
    user_avatar,
    guild_id_0,
    user_nick,
    user_guild_avatar,
    user_credibility,
    linked_quest_listing,
    page_index,
    current_date_time,
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
    
    guild_id_0 : `int`
        The respective guild's identifier the command was invoked at.
    
    user_nick : `int`
        The user's nick name.
    
    user_guild_avatar : ``None | Icon``
        The user's avatar in the guild.
    
    user_credibility : `int`
        The user's  credibility.
    
    linked_quest_listing : ``None | list<LinkedQuest>``
        The user's accepted quests.
    
    page_index : `int`
        The page's index to show.
    
    current_date_time : `DateTime`
        Current time use.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user = User.precreate(user_id, avatar = user_avatar, name = user_name)
    
    if guild_id_0 and ((user_nick is not None) or (user_guild_avatar is not None)):
        user.guild_profiles[guild_id_0] = GuildProfile(avatar = user_guild_avatar, nick = user_nick)
    
    user_stats = UserStats(user_id)
    user_stats.set('credibility', user_credibility)
    
    DateTimeMock.set_current(current_date_time)
    
    mocked = vampytest.mock_globals(
        build_linked_quests_listing_components,
        DateTime = DateTimeMock,
        recursion = 3,
    )
    
    output = mocked(user, guild_id_0, user_stats, linked_quest_listing, page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
