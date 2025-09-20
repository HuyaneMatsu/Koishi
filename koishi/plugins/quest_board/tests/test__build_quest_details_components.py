import vampytest

from hata import (
    BUILTIN_EMOJIS, ButtonStyle, Component, create_button, create_row, create_separator, create_text_display
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_CARROT, Quest, get_quest_template
from ...user_stats_core import UserStats

from ..component_building import build_quest_details_components


def _iter_options():
    user_id = 202505240000
    page_index = 5
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 3600
    
    
    yield (
        user_id,
        page_index,
        Quest(
            quest_template_id_0,
            quest_amount_0,
            3600,
            2,
            1000,
        ),
        1 << 6,
        [
            create_text_display(
                f'**Task: Submit {quest_amount_0/1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.**\n'
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
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Accept',
                    custom_id = f'quest_board.accept.{user_id:x}.{page_index:x}.{quest_template_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.item.{user_id:x}.{page_index:x}.{quest_template_id_0:x}.'
                        f'{quest_template_0.item_id:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_details_components(user_id, page_index, quest, credibility):
    """
    Tests whether ``build_quest_details_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
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

    output = build_quest_details_components(user_id, page_index, quest, user_stats)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
