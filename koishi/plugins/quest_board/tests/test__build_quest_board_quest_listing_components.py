import vampytest

from hata import (
    BUILTIN_EMOJIS, CDN_ENDPOINT, Component, Guild, Icon, IconType, create_button, create_row, create_section,
    create_separator, create_text_display, create_thumbnail_media
)

from ...guild_stats import GuildStats
from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, Quest,
    QuestBatch, get_quest_template
)

from ..component_building import build_quest_board_quest_listing_components
from ..constants import EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS


def _iter_options():
    guild_id = 202505230030
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template(quest_template_id_2)
    assert quest_template_2 is not None
    quest_amount_2 = 174000
    
    
    yield (
        guild_id,
        'Orin\'s dance house',
        Icon(IconType.static, 2),
        1 << 7,
        0,
        QuestBatch(
            123,
            (
                Quest(
                    quest_template_id_0,
                    quest_amount_0,
                    3600,
                    2,
                    1000,
                ),
                Quest(
                    quest_template_id_1,
                    quest_amount_1,
                    3600,
                    2,
                    1000,
                    
                ),
                Quest(
                    quest_template_id_2,
                    quest_amount_2,
                    3600,
                    2,
                    1000,
                ),
            )
        ),
        [
            create_section(
                create_text_display(
                    f'# Orin\'s dance house\'s quest board\n'
                    f'\n'
                    f'Guild rank: G\n'
                    f'Quest count: 3'
                ),
                thumbnail = create_thumbnail_media(
                    f'{CDN_ENDPOINT}/icons/{guild_id}/00000000000000000000000000000002.png',
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'Required rank: H\n'
                    f'Submit {quest_amount_0} Carrot {BUILTIN_EMOJIS["carrot"]} to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'quest_board.details.{quest_template_id_0:x}',
                ),
            ),
            create_section(
                create_text_display(
                    f'Required rank: G\n'
                    f'Submit {quest_amount_1} Peach {BUILTIN_EMOJIS["peach"]} to Mystia.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'quest_board.details.{quest_template_id_1:x}',
                ),
            ),
            create_section(
                create_text_display(
                    f'Required rank: G\n'
                    f'Submit {quest_amount_2 // 1000} kg Bluefrankish {BUILTIN_EMOJIS["grapes"]} to Sakuya.'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = f'quest_board.details.{quest_template_id_2:x}',
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    emoji = EMOJI_PAGE_PREVIOUS,
                    custom_id = 'quest_board.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    emoji = EMOJI_PAGE_NEXT,
                    custom_id = 'quest_board.page_increment_disabled',
                    enabled = False,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_board_quest_listing_components(
    guild_id, guild_name, guild_icon, credibility, page_index, quest_batch
):
    """
    Tests whether ``build_quest_board_quest_listing_components`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    guild_name : `str`
        The guild's name.
    
    guild_icon : ``None | Icon``
        The guild's icon.
    
    credibility : `int`
        The guild's  credibility.
    
    page_index : `int`
        The page's index to show.
    
    quest_batch : ``QuestBatch``
        Quest batch to return when requested.
    
    Returns
    -------
    output : ``list<Component>``
    """
    guild = Guild.precreate(guild_id, icon = guild_icon, name = guild_name)
    guild_stats = GuildStats(guild_id)
    guild_stats.set('credibility', credibility)
    
    
    def _patched_get_quest_batch(self):
        nonlocal quest_batch
        return quest_batch
    
    
    get_quest_batch_original = type(guild_stats).get_quest_batch
    type(guild_stats).get_quest_batch = _patched_get_quest_batch
    try:
        output = build_quest_board_quest_listing_components(guild, guild_stats, page_index)
    finally:
        type(guild_stats).get_quest_batch = get_quest_batch_original
    
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
