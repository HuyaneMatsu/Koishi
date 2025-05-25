import vampytest

from hata import BUILTIN_EMOJIS, Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_CARROT, Quest, get_quest_template
from ...user_stats_core import UserStats

from ..component_building import build_quest_details_components


def _iter_options():
    user_id = 202505240000
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    
    
    yield (
        Quest(
            quest_template_id_0,
            quest_amount_0,
            3600,
            2,
            1000,
        ),
        user_id,
        1 << 6,
        [
            create_text_display(
                f'**Task: Submit {quest_amount_0} Carrot {BUILTIN_EMOJIS["carrot"]} to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Reward:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'**Time available:**\n'
                f'- **1 hour**'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Accept',
                    custom_id = f'quest_board.accept.{quest_template_id_0:x}',
                ),
                create_button(
                    'Item information',
                    custom_id = f'quest_item.details.{quest_template_0.item_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_details_components(quest, user_id, credibility):
    """
    Tests whether ``build_quest_details_components`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest to describe.
    
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

    output = build_quest_details_components(quest, user_stats)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
