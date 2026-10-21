import vampytest
from hata import BUILTIN_EMOJIS, InteractionForm, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_CARROT
from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_CARROT, linked_quest_create, quest_requirement_serialisable_create_duration,
    quest_requirement_serialisable_create_expiration, quest_requirement_serialisable_create_item_exact,
    quest_reward_serialisable_create_balance, quest_reward_serialisable_create_credibility
)
from ...unit_core import AMOUNT_TYPE_WEIGHT
from ...user_stats_core import user_stats_create, user_stats_modify_credibility_by

from ..component_building import build_linked_quest_abandon_confirmation_form


def _iter_options():
    user_id = 202505240020
    guild_id = 202505240021
    
    quest_amount_0 = 3600
    
    linked_quest_0 = linked_quest_create(
        user_id,
        guild_id,
        5666,
        QUEST_TEMPLATE_ID_MYSTIA_CARROT,
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
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    page_index = 1
    
    yield (
        linked_quest_0,
        user_id,
        1 << 10,
        page_index,
        20,
        InteractionForm(
            'Please confirm abandoning',
            [
                create_text_display(
                    f'**Task: Submit 0 / {quest_amount_0 / 1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.**\n'
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
                create_text_display(
                    '-# You will lose 20 credibility upon abandoning this quest.'
                ),
            ],
            f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_abandon_confirmation_form(
    linked_quest, user_id, credibility, page_index, credibility_penalty
):
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
    
    credibility_penalty : `int`
        Abandon credibility penalty.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    def unix_time_seconds_get():
        return 1000000
    
    mocked = vampytest.mock_globals(
        build_linked_quest_abandon_confirmation_form,
        3,
        unix_time_seconds_get = unix_time_seconds_get,
    )
    
    user_stats = user_stats_create(user_id)
    user_stats_modify_credibility_by(user_stats, credibility)

    output = mocked(linked_quest, user_stats, page_index, credibility_penalty)
    
    vampytest.assert_instance(output, InteractionForm)
    
    return output
