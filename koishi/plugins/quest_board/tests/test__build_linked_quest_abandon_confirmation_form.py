import vampytest

from hata import BUILTIN_EMOJIS, InteractionForm, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, Quest, get_quest_template
from ...user_stats_core import UserStats

from ..component_building import build_linked_quest_abandon_confirmation_form


def _iter_options():
    user_id = 202505240020
    guild_id = 202505240021
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 3600
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        5666,
        Quest(
            quest_template_id_0,
            quest_amount_0,
            3600,
            10,
            1000,
        ),
    )
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    page_index = 1
    
    yield (
        linked_quest_0,
        user_id,
        1 << 10,
        page_index,
        InteractionForm(
            'Please confirm abandoning',
            [
                create_text_display(
                    f'**Task: Submit 0.00 / {quest_amount_0/1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.**\n'
                    f'\n'
                    f'I am running low on some vegetables for soups.\n'
                    f'\nRequesting a basketful of Carrot.\n'
                    f'\n'
                    f'**Reward:**\n'
                    f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                    f'- **5** credibility\n'
                    f'**Time available:**\n'
                    f'- **1 hour**\n'
                    f'**Time left:**\n'
                    f'- **59 minutes, 59 seconds**'
                ),
            ],
            f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_abandon_confirmation_form(linked_quest, user_id, credibility, page_index):
    """
    Tests whether ``build_linked_quest_abandon_confirmation_form`` works as intended.
    
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
    output : ``InteractionForm``
    """
    user_stats = UserStats(user_id)
    user_stats.set('credibility', credibility)

    output = build_linked_quest_abandon_confirmation_form(linked_quest, user_stats, page_index)
    
    vampytest.assert_instance(output, InteractionForm)
    
    return output
