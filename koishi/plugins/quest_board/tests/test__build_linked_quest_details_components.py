import vampytest

from hata import (
    BUILTIN_EMOJIS, ButtonStyle, Component, create_button, create_row, create_separator, create_text_display
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, Quest, get_quest_template
from ...user_stats_core import UserStats

from ..component_building import build_linked_quest_details_components


def _iter_options():
    user_id = 202505240020
    guild_id = 202505240021
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    
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
    
    
    yield (
        linked_quest_0,
        user_id,
        1 << 6,
        [
            create_text_display(
                f'**Task: Submit 0 / {quest_amount_0} Carrot {BUILTIN_EMOJIS["carrot"]} to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Reward:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Time left:**\n'
                f'- **59 minutes, 59 seconds**'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = f'linked_quest.submit.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Abandon quest',
                    custom_id = f'linked_quest.abandon.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Item information',
                    custom_id = f'quest_item.details.{quest_template_0.item_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_details_components(linked_quest, user_id, credibility):
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
    user_stats = UserStats(user_id)
    user_stats.set('credibility', credibility)

    output = build_linked_quest_details_components(linked_quest, user_stats)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
