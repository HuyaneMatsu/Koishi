__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import (
    ButtonStyle, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ..item_core import get_item_nullable
from ..quest_core import (
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, LINKED_QUEST_COMPLETION_STATE_COMPLETED, QUEST_TYPE_ITEM_SUBMISSION,
    get_guild_adventurer_rank_info, get_quest_template, get_user_adventurer_rank_info
)

from .constants import (
    CUSTOM_ID_LINKED_QUEST_ABANDON_FACTORY, CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY,
    CUSTOM_ID_LINKED_QUEST_ITEM_DISABLED, CUSTOM_ID_LINKED_QUEST_ITEM_FACTORY,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY, CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_FACTORY, CUSTOM_ID_QUEST_ACCEPT_DISABLED, CUSTOM_ID_QUEST_ACCEPT_FACTORY,
    CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED, CUSTOM_ID_QUEST_BOARD_ITEM_FACTORY,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY, CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, PAGE_SIZE
)
from .content_builders import (
    produce_linked_quest_detailed_description, produce_linked_quest_header_description,
    produce_linked_quest_short_description, produce_linked_quest_submit_success_completed_description,
    produce_linked_quest_submit_success_n_left_description, produce_nullable_item_description,
    produce_quest_board_header_description, produce_quest_detailed_description, produce_quest_short_description
)
from .helpers import get_linked_quest_for_deduplication


def build_quest_board_quest_listing_components(guild, guild_stats, user_stats, linked_quest_listing, page_index):
    """
    Builds quest board quest listing.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    
    guild_stats : ``GuildStats``
        The guild's stats.
    
    user_stats : ``UserStats``
        The user's stats.
    
    linked_quest_listing : : ``None | list<LinkedQuest>``
        The quests linked to the user.
    
    page_index : `int`
        The page's index to show.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add header.
    guild_adventurer_rank_info = get_guild_adventurer_rank_info(guild_stats.credibility)
    quest_batch = guild_stats.get_quest_batch()
    
    header_content_component = create_text_display(
        ''.join([*produce_quest_board_header_description(guild, guild_adventurer_rank_info, len(quest_batch.quests))]),
    )
    
    icon_url = guild.icon_url
    if (icon_url is None):
        component = header_content_component
    else:
        component = create_section(header_content_component, thumbnail = create_thumbnail_media(icon_url))
    
    components.append(component)
    
    components.append(create_separator())
    
    # Add quests.
    user_level = get_user_adventurer_rank_info(user_stats.credibility).level
    
    quest_slice = quest_batch.quests[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    if quest_slice:
        for quest in quest_slice:
            quest_template = get_quest_template(quest.template_id)
            linked_quest = get_linked_quest_for_deduplication(
                linked_quest_listing, guild.id, quest_batch.id, quest.template_id
            )
            
            if (linked_quest is not None) and (linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE):
                style = ButtonStyle.green
                custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(user_stats.user_id, 0, linked_quest.entry_id)
            
            else:
                if (
                    (quest_template is None) or
                    (quest_template.level > user_level)
                ):
                    style = ButtonStyle.gray
                elif linked_quest is None:
                    style = ButtonStyle.blue
                else:
                    repeat_count = quest_template.repeat_count
                    if repeat_count and (linked_quest.completion_count >= repeat_count):
                        style = ButtonStyle.gray
                    else:
                        style = ButtonStyle.blue
                
                custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY(
                    user_stats.user_id, page_index, (0 if quest_template is None else quest_template.id),
                )
            
            
            components.append(
                create_section(
                    create_text_display(
                        ''.join([*produce_quest_short_description(linked_quest, quest_template, quest.amount)])
                    ),
                    thumbnail = create_button(
                        'Details',
                        custom_id = custom_id,
                        enabled = (quest_template is not None),
                        style = style,
                    ),
                )
            )
        
        components.append(create_separator())
    
    # Add interactive components.
    quest_count = len(quest_batch.quests)
    if page_index == 0:
        button_page_index_decrement = create_button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED,
            enabled = False,
        )
    
    else:
        button_page_index_decrement = create_button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_stats.user_id, page_index - 1),
        )
    
    if quest_count <= (page_index + 1) * PAGE_SIZE:
        button_page_index_increment = create_button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
            enabled = False,
        )
    
    else:
        button_page_index_increment = create_button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_stats.user_id, page_index + 1),
        )
    
    components.append(
        create_row(
            button_page_index_decrement,
            button_page_index_increment,
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_stats.user_id, page_index),
            ),
        ),
    )
    
    return components


def build_quest_details_components(user_id, page_index, quest, linked_quest, user_stats):
    """
    Builds quest details components describing a quest of a quest board with more details.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest : ``Quest``
        The quest to describe.
    
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    user_stats : ``UserStats``
        The user's stats.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add quest description.
    quest_template = get_quest_template(quest.template_id)
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    components.append(
        create_text_display(
            ''.join([*produce_quest_detailed_description(quest, quest_template, user_adventurer_rank_info.level)]),
        ),
    )
    components.append(create_separator())
    
    if (
        (quest_template is None) or
        (quest_template.level > user_adventurer_rank_info.level)
    ):
        accept_enabled = False
    else:
        if (linked_quest is None):
            accept_enabled = True
        else:
            repeat_count = quest_template.repeat_count
            if repeat_count and (linked_quest.completion_count >= repeat_count):
                accept_enabled = False
            else:
                accept_enabled = True
    
    # Add interactive components.
    components.append(
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'Accept',
                custom_id = (
                    CUSTOM_ID_QUEST_ACCEPT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ACCEPT_FACTORY(user_id, page_index, quest_template.id)
                ),
                enabled = accept_enabled,
                style = (ButtonStyle.green if accept_enabled else ButtonStyle.gray),
            ),
            create_button(
                'Item information',
                custom_id = (
                    CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_BOARD_ITEM_FACTORY(user_id, page_index, quest_template.id, quest_template.item_id)
                ),
                enabled = (quest_template is not None),
            ),
        ),
    )
    
    return components


def build_quest_accept_success_components(user_id, page_index, linked_quest_entry_id):
    """
    Builds response components when a quest is successfully accepted.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The page's index to show.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You successfully accepted the quest.'),
        create_separator(),
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_id, 0),
            ),
            create_button(
                'View the quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(user_id, 0, linked_quest_entry_id),
                style = ButtonStyle.green,
            ),
        ),
    ]


def _linked_quest_sort_key_getter(linked_quest):
    """
    Gets sort key for linked quest.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to get sort key for.
    
    Returns
    -------
    sort_key : `(int, int, int)`
    """
    completion_count = linked_quest.completion_count
    completion_state = linked_quest.completion_state
    quest_template = get_quest_template(linked_quest.template_id)
    if quest_template is None:
        repeat_count = -1
    else:
        repeat_count = quest_template.repeat_count
    
    if completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
        completion_state_weight = 1
    elif completion_state == LINKED_QUEST_COMPLETION_STATE_COMPLETED:
        completion_state_weight = 2
    else:
        completion_state_weight = 3
    
    if repeat_count == -1:
        repeat_weight = 4
    elif repeat_count == 0:
        repeat_weight = 1
    elif completion_count < repeat_count:
        repeat_weight = 2
    else:
        repeat_weight = 3
    
    if repeat_count == -1:
        completion_count_weight = 1
    else:
        completion_count_weight = -repeat_count
    
    return (
        completion_state_weight,
        repeat_weight,
        completion_count_weight,
    )


def build_linked_quests_listing_components(user, guild_id, user_stats, linked_quest_listing, page_index):
    """
    Builds linked quest listing.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    
    guild_id : `int`
        The respective guild's identifier the command was invoked at.
    
    user_stats : ``UserStats``
        The user's stats.
    
    linked_quest_listing : ``None | list<LinkedQuest>``
        The user's accepted quests.
    
    page_index : `int`
        The page's index to show.
    
    Returns
    -------
    components : ``list<Component>``
    """
    # Normalize quests
    if (linked_quest_listing is None):
        linked_quest_listing_sorted = None
    else:
        linked_quest_listing_sorted = sorted(linked_quest_listing, key = _linked_quest_sort_key_getter)
    
    components = []
    
    # Add header.
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    components.append(
        create_section(
            create_text_display(
                ''.join([*produce_linked_quest_header_description(
                    user,
                    guild_id,
                    user_adventurer_rank_info,
                    (
                        0
                        if (linked_quest_listing is None) else
                        sum(
                            linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE
                            for linked_quest in linked_quest_listing
                        )
                    ),
                )])
            ),
            thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
        ),
    )
    components.append(create_separator())
    
    # Add linked quests.
    if (linked_quest_listing is not None):
        linked_quest_slice = linked_quest_listing_sorted[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
        if linked_quest_slice:
            for linked_quest in linked_quest_slice:
                quest_template = get_quest_template(linked_quest.template_id)
                
                if linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
                    style = ButtonStyle.green
                    custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(
                        user.id, page_index, linked_quest.entry_id
                    )
                    enabled = True
                
                else:
                    if (
                        (quest_template is None) or
                        (quest_template.level > user_adventurer_rank_info.level)
                    ):
                        style = ButtonStyle.gray
                    else:
                        repeat_count = quest_template.repeat_count
                        if repeat_count and (linked_quest.completion_count >= repeat_count):
                            style = ButtonStyle.gray
                        else:
                            style = ButtonStyle.blue
                    
                    enabled = guild_id == linked_quest.guild_id
                    custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY(
                        user.id, 0, (0 if quest_template is None else quest_template.id),
                    )
                
                components.append(
                    create_section(
                        create_text_display(
                            ''.join([*produce_linked_quest_short_description(linked_quest, quest_template)])
                        ),
                        thumbnail = create_button(
                            'Details',
                            custom_id = custom_id,
                            enabled = enabled,
                            style = style,
                        ),
                    )
                )
            
            components.append(create_separator())
    
    # Add interactive components.
    quest_count = 0 if linked_quest_listing is None else len(linked_quest_listing)
    if page_index == 0:
        button_page_index_decrement = create_button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED,
            enabled = False,
        )
    
    else:
        button_page_index_decrement = create_button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user.id, page_index - 1),
        )
    
    if quest_count <= (page_index + 1) * PAGE_SIZE:
        button_page_index_increment = create_button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
            enabled = False,
        )
    
    else:
        button_page_index_increment = create_button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user.id, page_index + 1),
        )
    
    components.append(
        create_row(
            button_page_index_decrement,
            button_page_index_increment,
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user.id, 0),
                enabled = (True if guild_id else False),
            ),
        ),
    )
    
    return components


def build_linked_quest_details_components(linked_quest, user_stats, page_index):
    """
    Builds linked quest details components describing the accepted quest in details.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to describe.
    
    user_stats : ``UserStats``
        The user's stats.
    
    page_index : `int`
        Page index to direct back to.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add quest description.
    quest_template = get_quest_template(linked_quest.template_id)
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    components.append(
        create_text_display(
            ''.join([*produce_linked_quest_detailed_description(
                linked_quest, quest_template, user_adventurer_rank_info.level
            )]),
        ),
    )
    
    components.append(create_separator())
    
    # Add interactive components.
    if (quest_template is None) or (linked_quest.expires_at < DateTime.now(tz = TimeZone.utc)):
        submit_button_enabled = False
        submit_button_style = ButtonStyle.gray
        abandon_quest_style = ButtonStyle.blue
    else:
        submit_button_enabled = (quest_template.type == QUEST_TYPE_ITEM_SUBMISSION)
        submit_button_style = ButtonStyle.green
        abandon_quest_style = ButtonStyle.red
    
    components.append(
        create_row(
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_stats.user_id, page_index),
            ),
            create_button(
                'Submit items',
                custom_id = (
                    CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_LINKED_QUEST_SUBMIT_FACTORY(user_stats.user_id, page_index, linked_quest.entry_id)
                ),
                enabled = submit_button_enabled,
                style = submit_button_style,
            ),
            create_button(
                'Abandon quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_FACTORY(
                    user_stats.user_id, page_index, linked_quest.entry_id
                ),
                style = abandon_quest_style,
            ),
            create_button(
                'Item information',
                custom_id = (
                    CUSTOM_ID_LINKED_QUEST_ITEM_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_LINKED_QUEST_ITEM_FACTORY(
                        user_stats.user_id, page_index, linked_quest.entry_id, quest_template.item_id
                    )
                ),
                enabled = (quest_template is not None),
            ),
        ),
    )
    
    return components


def build_linked_quest_abandon_success_components(user_id, page_index, guild_id):
    """
    Builds successfully abandoning response components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You successfully abandoned the quest.'),
        create_separator(),
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_id, 0),
                enabled = (True if guild_id else False),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
        ),
    ]


def build_linked_quest_submit_success_n_left_components(
    user_id, page_index, linked_quest_entry_id, item, amount_type, amount_submitted, amount_required, amount_used
):
    """
    Builds successful item submission components when `n` items are still left to submit.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_submitted : `int`
        Already submitted amount.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_linked_quest_submit_success_n_left_description(
                item, amount_type, amount_submitted, amount_required, amount_used,
            )]),
        ),
        create_separator(),
        create_row(
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'Back to the quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(user_id, page_index, linked_quest_entry_id),
            ),
        ),
    ]


def build_linked_quest_submit_success_completed_components(
    user_id,
    page_index,
    guild_id,
    linked_quest,
    quest_template,
    user_stats,
    user_level_old,
    item,
    amount_type,
    amount_required,
    amount_used,
    reward_credibility,
):
    """
    Builds successful item submission components when all the required items were submitted.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    linked_quest : : ``LinkedQuest``
        The finished quest.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    user_stats : ``UserStats``
        The user's stats.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    Returns
    -------
    components : ``list<Component>``
    """
    user_level_new = get_user_adventurer_rank_info(user_stats.credibility).level
    
    components = []
    
    # Description
    components.append(create_text_display(
        ''.join([*produce_linked_quest_submit_success_completed_description(
            item,
            amount_type,
            amount_required,
            amount_used,
            linked_quest.reward_balance,
            reward_credibility,
            user_level_old,
            user_level_new,
        )]),
    ))
    
    # Control
    components.append(create_separator())
    
    while True:
        if linked_quest.entry_id == 0:
            repeat_enabled = False
            repeat_style = ButtonStyle.gray
            break
        
        repeat_count = quest_template.repeat_count
        if repeat_count and (repeat_count <= linked_quest.completion_count):
            repeat_enabled = False
            repeat_style = ButtonStyle.gray
            break
        
        if (quest_template.level > user_level_new):
            repeat_enabled = False
            repeat_style = ButtonStyle.gray
            break
        
        repeat_enabled = True
        repeat_style = (ButtonStyle.green if linked_quest.guild_id == guild_id else ButtonStyle.gray)
        break
    
    components.append(
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_id, 0),
                enabled = (True if guild_id else False),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'Repeat',
                custom_id = (
                    CUSTOM_ID_QUEST_ACCEPT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ACCEPT_FACTORY(user_id, 0, quest_template.id)
                ),
                enabled = repeat_enabled,
                style = repeat_style,
            ),
        ),
    )
    
    return components


def build_quest_board_item_components(user_id, page_index, quest_template_id, item_id):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_nullable_item_description(get_item_nullable(item_id))])),
        create_separator(),
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'Back to the quest',
                custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY(user_id, page_index, quest_template_id),
            ),
        ),
    ]


def build_linked_quest_item_components(user_id, page_index, linked_quest_entry_id, item_id):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests's current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_nullable_item_description(get_item_nullable(item_id))])),
        create_separator(),
        create_row(
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY(user_id, page_index),
            ),
            create_button(
                'Back to the quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(user_id, page_index, linked_quest_entry_id),
            ),
        ),
    ]
