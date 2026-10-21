import vampytest

from hata import (
    ButtonStyle, Component, create_button, create_row, create_separator, create_text_display
)

from ...item_core import ITEM_ID_CARROT, ITEM_ID_PEACH, get_item_nullable
from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_CARROT, linked_quest_create, quest_requirement_serialisable_create_duration,
    quest_requirement_serialisable_create_expiration, quest_requirement_serialisable_create_item_exact,
    quest_reward_serialisable_create_balance, quest_reward_serialisable_create_credibility
)
from ...unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT
from ...user_stats_core import user_stats_create, user_stats_modify_credibility_by

from ..component_building import build_linked_quest_details_components


def _iter_options():
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert (item_carrot is not None)
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert (item_peach is not None)
    
    user_id = 202505240020
    guild_id = 202505240021
    
    linked_quest_0 = linked_quest_create(
        user_id,
        guild_id,
        5666,
        QUEST_TEMPLATE_ID_MYSTIA_CARROT,
        (
            quest_requirement_serialisable_create_duration(3600),
            quest_requirement_serialisable_create_expiration(1000000 + 3600),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 3600, 0),
        ),
        (
            quest_reward_serialisable_create_balance(1000),
            quest_reward_serialisable_create_credibility(10),
        ),
    )
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    
    linked_quest_1 = linked_quest_create(
        user_id,
        guild_id,
        5666,
        QUEST_TEMPLATE_ID_MYSTIA_CARROT,
        (
            quest_requirement_serialisable_create_duration(3600),
            quest_requirement_serialisable_create_expiration(1000000 + 3600),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 3600, 0),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
        ),
        (
            quest_reward_serialisable_create_balance(1000),
            quest_reward_serialisable_create_credibility(10),
        ),
    )
    linked_quest_entry_id_1 = 124
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    page_index = 1
    
    yield (
        linked_quest_0,
        user_id,
        1 << 10,
        page_index,
        [
            create_text_display(
                f'**Task:** Submit **0 / {3600 / 1000} kg {item_carrot.emoji} {item_carrot.name}** to Mystia.\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Time left:**\n'
                f'- **1 hour**\n'
                f'**Completed:**\n'
                f'- **0 / 3** times, cannot be re-accepted anymore'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Abandon',
                    custom_id = f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Auto submit items',
                    custom_id = f'linked_quest.submit_auto.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Select requirement to submit for',
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}.'
                        f'{0:x}'
                    ),
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )
    
    yield (
        linked_quest_1,
        user_id,
        1 << 10,
        page_index,
        [
            create_text_display(
                f'**Task:** Submit **0 / {3600 / 1000} kg {item_carrot.emoji} {item_carrot.name}** and '
                f'**0 / 20 {item_peach.emoji} {item_peach.name}** to Mystia.\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Time left:**\n'
                f'- **1 hour**\n'
                f'**Completed:**\n'
                f'- **0 / 3** times, cannot be re-accepted anymore'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Abandon',
                    custom_id = f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_1:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Auto submit items',
                    custom_id = f'linked_quest.submit_auto.{user_id:x}.{page_index:x}.{linked_quest_entry_id_1:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                'Select requirement to submit for',
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{page_index:x}.'
                        f'{linked_quest_entry_id_1:x}.{0:x}'
                    ),
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_details_components(linked_quest, user_id, credibility, page_index):
    """
    Tests whether ``build_linked_quest_details_components`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to describe.
    
    user_id : `int`
        The guild's identifier.
    
    credibility : `int`
        The user's  credibility.
    
    Returns
    -------
    output : ``list<Component>``
    """
    def unix_time_seconds_get():
        return 1000000
    
    mocked = vampytest.mock_globals(
        build_linked_quest_details_components,
        3,
        unix_time_seconds_get = unix_time_seconds_get,
    )
    
    user_stats = user_stats_create(user_id)
    user_stats_modify_credibility_by(user_stats, credibility)

    output = mocked(linked_quest, user_stats, page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
