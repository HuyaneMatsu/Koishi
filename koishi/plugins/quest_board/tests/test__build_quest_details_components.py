from math import ceil

import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...inventory_core import Inventory
from ...item_core import ITEM_ID_CARROT, get_item_nullable
from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, QUEST_TEMPLATE_ID_MYSTIA_CARROT, quest_create,
    get_quest_template_nullable, linked_quest_create, quest_requirement_instantiable_create_duration,
    quest_requirement_instantiable_create_item_exact, quest_requirement_serialisable_create_duration,
    quest_requirement_serialisable_create_expiration, quest_requirement_serialisable_create_item_exact,
    quest_reward_instantiable_create_balance, quest_reward_instantiable_create_credibility,
    quest_reward_serialisable_create_balance, quest_reward_serialisable_create_credibility
)
from ...unit_core import AMOUNT_TYPE_WEIGHT
from ...user_stats_core import user_stats_create, user_stats_modify_credibility_by

from ..component_building import build_quest_details_components


def _iter_options():
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert item_carrot is not None
    
    user_id = 202505240000
    guild_id_0 = 202510120003
    guild_id_1 = 202510260000
    batch_id = 1566
    
    page_index = 5
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template_nullable(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 3600
    
    quest = quest_create(
        quest_template_id_0,
        (
            quest_requirement_instantiable_create_duration(3600),
            quest_requirement_instantiable_create_item_exact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, quest_amount_0),
        ),
        (
            quest_reward_instantiable_create_balance(1000),
            quest_reward_instantiable_create_credibility(10),
        ),
    )
    
    linked_quest = linked_quest_create(
        user_id,
        guild_id_0,
        batch_id,
        quest_template_id_0,
        (
            quest_requirement_serialisable_create_duration(3600),
            quest_requirement_serialisable_create_expiration(1000000 + 3600),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, quest_amount_0, 0),
        ),
        (
            quest_reward_serialisable_create_balance(1000),
            quest_reward_serialisable_create_credibility(10),
        ),
    )
    linked_quest.completion_count = 3
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    
    inventory_0 = Inventory(user_id)
    
    inventory_1 = Inventory(user_id)
    inventory_1.modify_item_amount(item_carrot, ceil(quest_amount_0 / item_carrot.weight) << 1)
    
    yield (
        'to complete',
        user_id,
        guild_id_0,
        guild_id_0,
        page_index,
        quest,
        None,
        inventory_0,
        1 << 10,
        [
            create_text_display(
                f'**Task: Submit {quest_amount_0 / 1000} kg {item_carrot.emoji} {item_carrot.name} to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Completable:**\n'
                f'- **3** times'
            ),
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
                    'Select requirement to inspect',
                    custom_id = (
                        f'quest_board.select_requirement.{user_id:x}.{guild_id_0:x}.{page_index:x}.'
                        f'{quest_template_id_0:x}.{0:x}'
                    ),
                ),
            ),
        ],
    )
    
    yield (
        'completed',
        user_id,
        guild_id_0,
        guild_id_1,
        page_index,
        quest,
        linked_quest,
        inventory_0,
        1 << 10,
        [
            create_text_display(
                f'**Task: Submit {quest_amount_0 / 1000} kg {item_carrot.emoji} {item_carrot.name} to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Completable:**\n'
                f'- **3** times (**0** left)'
            ),
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
                    'Select requirement to inspect',
                    custom_id = (
                        f'quest_board.select_requirement.{user_id:x}.{guild_id_0:x}.{page_index:x}.'
                        f'{quest_template_id_0:x}.{0:x}'
                    ),
                ),
            ),
        ],
    )
    
    yield (
        'to complete, possessed x2',
        user_id,
        guild_id_0,
        guild_id_0,
        page_index,
        quest,
        None,
        inventory_1,
        1 << 10,
        [
            create_text_display(
                f'**Task: Submit {quest_amount_0 / 1000} kg {item_carrot.emoji} {item_carrot.name} to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Completable:**\n'
                f'- **3** times (**2** times in possession)'
            ),
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
                    'Select requirement to inspect',
                    custom_id = (
                        f'quest_board.select_requirement.{user_id:x}.{guild_id_0:x}.{page_index:x}.'
                        f'{quest_template_id_0:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Complete',
                    custom_id = (
                        f'quest_board.complete.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id_0:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__build_quest_details_components(
    user_id, guild_id, local_guild_id, page_index, quest, linked_quest, inventory, credibility
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
    
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    user_id : `int`
        The guild's identifier.
    
    credibility : `int`
        The user's  credibility.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user_stats = user_stats_create(user_id)
    user_stats_modify_credibility_by(user_stats, credibility)

    output = build_quest_details_components(
        user_id, guild_id, local_guild_id, page_index, quest, linked_quest, inventory, user_stats
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
