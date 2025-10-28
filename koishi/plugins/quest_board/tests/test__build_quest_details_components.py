import vampytest

from hata import (
    BUILTIN_EMOJIS, ButtonStyle, Component, create_button, create_row, create_separator, create_text_display
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, Quest, get_quest_template
)
from ...user_stats_core import UserStats

from ..component_building import build_quest_details_components


def _iter_options():
    user_id = 202505240000
    guild_id_0 = 202510120003
    guild_id_1 = 202510260000
    batch_id = 1566
    
    page_index = 5
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 3600
    
    quest = Quest(
        quest_template_id_0,
        quest_amount_0,
        3600,
        10,
        1000,
    )
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id_0,
        batch_id,
        quest,
    )
    linked_quest.completion_count = 3
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    quest_description = (
        f'**Task: Submit {quest_amount_0/1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.**\n'
        f'\n'
        f'I am running low on some vegetables for soups.\n'
        f'\nRequesting a basketful of Carrot.\n'
        f'\n'
        f'**Reward:**\n'
        f'- **1000** {EMOJI__HEART_CURRENCY}\n'
        f'- **5** credibility\n'
        f'**Time available:**\n'
        f'- **1 hour**'
    )
    
    yield (
        user_id,
        guild_id_0,
        guild_id_0,
        page_index,
        quest,
        None,
        1 << 10,
        [
            create_text_display(quest_description),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{page_index:x}',
                    enabled = True,
                ),
                create_button(
                    'Accept',
                    custom_id = f'quest_board.accept.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id_0:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.item.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id_0:x}.'
                        f'{quest_template_0.item_id:x}'
                    ),
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        guild_id_0,
        guild_id_1,
        page_index,
        quest,
        linked_quest,
        1 << 10,
        [
            create_text_display(quest_description),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{page_index:x}',
                    enabled = False,
                ),
                create_button(
                    'Accept',
                    custom_id = f'quest_board.accept.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id_0:x}',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.item.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id_0:x}.'
                        f'{quest_template_0.item_id:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_details_components(
    user_id, guild_id, local_guild_id, page_index, quest, linked_quest, credibility
):
    """
    Tests whether ``build_quest_details_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The parent quest's guild's identifier.
    
    local_guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest : ``Quest``
        The quest to describe.
    
    linked_quest : : ``None LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    user_id : `int`
        The guild's identifier.
    
    credibility : `int`
        The user's  credibility.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user_stats = UserStats(user_id)
    user_stats.set('credibility', credibility)

    output = build_quest_details_components(
        user_id, guild_id, local_guild_id, page_index, quest, linked_quest, user_stats
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
