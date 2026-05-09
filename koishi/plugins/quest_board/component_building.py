__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import (
    ButtonStyle, InteractionForm, create_button, create_label, create_row, create_section, create_separator,
    create_text_display, create_text_input, create_thumbnail_media
)

from ..item_core import get_item_group_nullable, get_item_nullable
from ..quest_core import (
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, LINKED_QUEST_COMPLETION_STATE_COMPLETED, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP, get_guild_adventurer_rank_info,
    get_quest_template_nullable, get_user_adventurer_rank_info
)

from .constants import (
    BACK_DIRECT_LOCATION_QUEST, BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED, BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
    BACK_DIRECT_LOCATION_SELECT_REQUIREMENT, EMOJI_BACK, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, EMOJI_REFRESH, PAGE_SIZE,
    REQUIREMENT_PAGE_SIZE
)
from .content_building import (
    produce_linked_quest_detailed_description, produce_linked_quest_header_description,
    produce_linked_quest_short_description, produce_linked_quest_submission_item_select_description,
    produce_linked_quest_submission_item_select_header, produce_linked_quest_submit_success,
    produce_linked_quest_submit_success_completed_description, produce_nullable_item_description,
    produce_nullable_item_group_description, produce_quest_board_header_description, produce_quest_detailed_description,
    produce_quest_details_base_section, produce_quest_short_description,
    produce_submission_requirements_entry_description
)
from .custom_ids import (
    CUSTOM_ID_COMPLETION_COUNT, CUSTOM_ID_LINKED_QUEST_ABANDON_BUILDER, CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER, CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_BUILDER, CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_GROUP_REQUIREMENT_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_BUILDER, CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_REQUIREMENT_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_BUILDER, CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER, CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_QUEST_ACCEPT_BUILDER,
    CUSTOM_ID_QUEST_ACCEPT_DISABLED, CUSTOM_ID_QUEST_BOARD_COMPLETE_BUILDER,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER, CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER,
    CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_GROUP_REQUIREMENT_BUILDER, CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_REQUIREMENT_BUILDER,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_BUILDER,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED
)
from .helpers import (
    get_allowed_completion_count, get_linked_quest_expiration, get_linked_quest_for_deduplication,
    get_linked_quest_submission_requirements_normalised, get_quest_in_possession_count,
    get_quest_submission_requirements_normalised, iter_submission_requirement_item_entries_of_normalised
)


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
    quest_batch = guild_stats.get_quest_batch()
    credibility = guild_stats.credibility
    guild_adventurer_rank_info = get_guild_adventurer_rank_info(credibility)
    
    header_content_component = create_text_display(
        ''.join([*produce_quest_board_header_description(
            guild, credibility, guild_adventurer_rank_info, len(quest_batch.quests)
        )]),
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
            quest_template = get_quest_template_nullable(quest.template_id)
            linked_quest = get_linked_quest_for_deduplication(
                linked_quest_listing, guild.id, quest_batch.id, quest.template_id
            )
            
            if (linked_quest is not None) and (linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE):
                style = ButtonStyle.green
                custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(user_stats.user_id, 0, linked_quest.entry_id)
            
            else:
                if (
                    (quest_template is None) or
                    (quest_template.level > user_level + 1)
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
                
                custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER(
                    user_stats.user_id, guild.id, page_index, (0 if quest_template is None else quest_template.id),
                )
            
            
            components.append(
                create_section(
                    create_text_display(
                        ''.join([*produce_quest_short_description(linked_quest, quest, quest_template)])
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
        custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_stats.user_id, page_index - 1)
        enabled = True
    
    button_page_index_decrement = create_button(
        f'Page {page_index!s}',
        EMOJI_PAGE_PREVIOUS,
        custom_id = custom_id,
        enabled = enabled
    )
    
    if quest_count <= (page_index + 1) * PAGE_SIZE:
        custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_stats.user_id, page_index + 1)
        enabled = True
    
    button_page_index_increment = create_button(
        f'Page {page_index + 2!s}',
        EMOJI_PAGE_NEXT,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    components.append(
        create_row(
            button_page_index_decrement,
            button_page_index_increment,
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_stats.user_id, 0),
            ),
        ),
    )
    
    return components


def build_quest_details_components(
    user_id, guild_id, local_guild_id, page_index, quest, linked_quest, inventory, user_stats
):
    """
    Builds quest details components describing a quest of a quest board with more details.
    
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
    
    user_stats : ``UserStats``
        The user's stats.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add quest description.
    quest_template = get_quest_template_nullable(quest.template_id)
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    completion_count = (0 if linked_quest is None else linked_quest.completion_count)
    possession_count = get_quest_in_possession_count(quest, inventory)
    
    components.append(
        create_text_display(
            ''.join([*produce_quest_detailed_description(
                quest, quest_template, user_adventurer_rank_info.level, completion_count, possession_count
            )]),
        ),
    )
    components.append(create_separator())
    
    if (
        (quest_template is None) or
        (quest_template.level > user_adventurer_rank_info.level + 1)
    ):
        accept_enabled = False
    
    else:
        repeat_count = quest_template.repeat_count
        if repeat_count and (completion_count >= repeat_count):
            accept_enabled = False
        else:
            accept_enabled = True
    
    # Extra requirement
    has_submission_requirement = False
    requirements = quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE in (
                QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
                QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
                QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
            ):
                has_submission_requirement = True
                break
    
    
    if not has_submission_requirement:
        extra_requirement_components = ()
    
    else:
        extra_requirement_components = (
            create_button(
                'Select requirement to inspect',
                custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_BUILDER(
                    user_id, guild_id, page_index, quest_template.id, 0
                ),
            ),
        )
    
    # Extra complete
    if not (accept_enabled and possession_count):
        extra_accept_components = ()
    
    else:
        extra_accept_components = (
            create_button(
                'Complete',
                custom_id = CUSTOM_ID_QUEST_BOARD_COMPLETE_BUILDER(user_id, guild_id, page_index, quest_template.id),
                style = ButtonStyle.green,
            ),
        )
    
    # Add interactive components.
    components.append(
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index),
                enabled = (guild_id == local_guild_id),
            ),
            create_button(
                'Accept',
                custom_id = (
                    CUSTOM_ID_QUEST_ACCEPT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ACCEPT_BUILDER(user_id, guild_id, page_index, quest_template.id)
                ),
                enabled = accept_enabled,
                style = (ButtonStyle.green if accept_enabled else ButtonStyle.gray),
            ),
            *extra_requirement_components,
            *extra_accept_components,
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
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_id, 0),
            ),
            create_button(
                'View the quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(user_id, 0, linked_quest_entry_id),
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
    sort_key : `(int, int, int, int)`
    """
    # Get basic fields
    completion_count = linked_quest.completion_count
    completion_state = linked_quest.completion_state
    
    quest_template = get_quest_template_nullable(linked_quest.template_id)
    if quest_template is None:
        repeat_count = -1
    else:
        repeat_count = quest_template.repeat_count
    
    expiration = get_linked_quest_expiration(linked_quest)
    
    # First sort: by completion state
    # - active
    # - completed
    # - other
    
    if completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
        completion_state_weight = 1
    elif completion_state == LINKED_QUEST_COMPLETION_STATE_COMPLETED:
        completion_state_weight = 2
    else:
        completion_state_weight = 3
    
    # Second sort: when teh quest expires
    # - active with expiration
    # - other
    if (completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE) and (expiration is not None):
        expiration_weight = int(expiration.timestamp())
    else:
        expiration_weight = (1 << 63) - 1
    
    # Third sort: whether the quest can be repeated; non repeatable comes first.
    # - unlimited
    # - limited
    # - on last completion / other
    
    if repeat_count == 0:
        repeat_weight = 1
    elif completion_count < repeat_count:
        repeat_weight = 2
    else:
        repeat_weight = 3
    
    # Fourth sort: How much times the quest can be repeated.
    # - limited -> negate count
    # - unlimited
    
    if repeat_count == 0:
        completion_count_weight = 1
    else:
        completion_count_weight = -repeat_count
    
    return (
        completion_state_weight,
        expiration_weight,
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
    credibility = user_stats.credibility
    user_adventurer_rank_info = get_user_adventurer_rank_info(credibility)
    components.append(
        create_section(
            create_text_display(
                ''.join([*produce_linked_quest_header_description(
                    user,
                    guild_id,
                    credibility,
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
            now = DateTime.now(TimeZone.utc)
            
            for linked_quest in linked_quest_slice:
                quest_template = get_quest_template_nullable(linked_quest.template_id)
                
                while True:
                    expiration = get_linked_quest_expiration(linked_quest)
                    if (expiration is not None) and (expiration <= now):
                        style = ButtonStyle.red
                        break
                    
                    if linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
                        style = ButtonStyle.green
                        break
                    
                    if (
                        (quest_template is None) or
                        (quest_template.level > user_adventurer_rank_info.level + 1)
                    ):
                        style = ButtonStyle.gray
                        break
                    
                    repeat_count = quest_template.repeat_count
                    if repeat_count and (linked_quest.completion_count >= repeat_count):
                        style = ButtonStyle.gray
                        break
                    
                    style = ButtonStyle.blue
                    break
                
                
                if linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
                    custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(
                        user.id, page_index, linked_quest.entry_id
                    )
                else:
                    custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER(
                        user.id, linked_quest.guild_id, 0, (0 if quest_template is None else quest_template.id),
                    )
                
                components.append(
                    create_section(
                        create_text_display(
                            ''.join([*produce_linked_quest_short_description(linked_quest, quest_template)])
                        ),
                        thumbnail = create_button(
                            'Details',
                            custom_id = custom_id,
                            enabled = True,
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
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user.id, page_index - 1),
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
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user.id, page_index + 1),
        )
    
    components.append(
        create_row(
            button_page_index_decrement,
            button_page_index_increment,
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user.id, 0),
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
    quest_template = get_quest_template_nullable(linked_quest.template_id)
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    components.append(
        create_text_display(
            ''.join([*produce_linked_quest_detailed_description(
                linked_quest, quest_template, user_adventurer_rank_info.level
            )]),
        ),
    )
    
    components.append(create_separator())
    
    has_submission_requirement = False
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE in (
                QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
                QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
                QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
            ):
                has_submission_requirement = True
                break
    
    
    if not has_submission_requirement:
        extra_control_components = ()
    
    else:
        extra_control_components = (
            create_button(
                'Auto submit items',
                custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_BUILDER(
                    user_stats.user_id, page_index, linked_quest.entry_id
                ),
                style = ButtonStyle.green,
            ),
            create_button(
                'Select requirement to submit for',
                custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
                    user_stats.user_id, page_index, linked_quest.entry_id, 0
                ),
                style = ButtonStyle.green,
            ),
        )
    
    
    components.append(
        create_row(
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_stats.user_id, page_index),
            ),
            create_button(
                'Abandon',
                custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_BUILDER(
                    user_stats.user_id, page_index, linked_quest.entry_id
                ),
                style = ButtonStyle.red,
            ),
            *extra_control_components,
        ),
    )
    
    return components


def build_linked_quest_abandon_confirmation_form(linked_quest, user_stats, page_index, credibility_penalty):
    """
    Builds quest abandon confirmation form.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to abandon.
    
    user_stats : ``UserStats``
        The user's stats.
    
    page_index : `int`
        The linked quests' current page's index.
    
    credibility_penalty : `int`
        Abandon credibility penalty.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    quest_template = get_quest_template_nullable(linked_quest.template_id)
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    # Build components
    components = []
    
    # Description
    components.append(
        create_text_display(
            ''.join([*produce_linked_quest_detailed_description(
                linked_quest, quest_template, user_adventurer_rank_info.level
            )]),
        ),
    )
    
    # Credibility penalty
    if credibility_penalty:
        components.append(
            create_text_display(
                f'-# You will lose {credibility_penalty!s} credibility upon abandoning this quest.'
            ),
        )
    
    # Build form
    return InteractionForm(
        'Please confirm abandoning',
        components,
        CUSTOM_ID_LINKED_QUEST_ABANDON_BUILDER(
            user_stats.user_id, page_index, linked_quest.entry_id
        ),
    )


def build_linked_quest_abandon_success_components(user_id, page_index, guild_id, credibility_penalty):
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
    
    credibility_penalty : `int`
        Abandon credibility penalty.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if credibility_penalty:
        description = f'You successfully abandoned the quest, losing {credibility_penalty!s} credibility.'
    else:
        description = 'You successfully abandoned the quest.'
    
    return [
        create_text_display(description),
        create_separator(),
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_id, 0),
                enabled = (True if guild_id else False),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index),
            ),
        ),
    ]


def _get_quest_board_back_direct_custom_id(
    user_id,
    guild_id,
    page_index,
    quest_template_id,
    requirement_index,
    back_direct_location,
):
    """
    get quest board submission back-direct custom identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The parent quest's guild's identifier.
    
    page_index : `int`
        The quest boards' current page's index.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    Returns
    -------
    custom_id : `str`
    """
    if back_direct_location == BACK_DIRECT_LOCATION_QUEST:
        custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER(user_id, guild_id, page_index, quest_template_id)
    
    elif back_direct_location == BACK_DIRECT_LOCATION_SELECT_REQUIREMENT:
        custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_BUILDER(
            user_id, guild_id, page_index, quest_template_id, requirement_index // REQUIREMENT_PAGE_SIZE
        )
    
    else:
        # No other case, redirect to the quest.
        custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER(user_id, page_index, quest_template_id)
    
    return custom_id


def _get_linked_quest_submission_back_direct_custom_id(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
):
    """
    get linked quest submission back-direct custom identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    item_page_index : `int`
        The items' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    Returns
    -------
    custom_id : `str`
    """
    if back_direct_location == BACK_DIRECT_LOCATION_QUEST:
        custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(user_id, page_index, linked_quest_entry_id)
    
    elif back_direct_location == BACK_DIRECT_LOCATION_SELECT_REQUIREMENT:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
            user_id, page_index, linked_quest_entry_id, requirement_index // REQUIREMENT_PAGE_SIZE
        )
    
    elif back_direct_location == BACK_DIRECT_LOCATION_SELECT_ITEM_TOP:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER(
            user_id, page_index, linked_quest_entry_id, item_page_index
        )
    
    elif back_direct_location == BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER(
            user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index
        )
    
    else:
        # No other case, redirect to the quest.
        custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(user_id, page_index, linked_quest_entry_id)
    
    return custom_id


def build_linked_quest_submit_success(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
    submissions_normalised,
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
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    item_page_index : `int`
        The items' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_linked_quest_submit_success(submissions_normalised)]),
        ),
        create_separator(),
        create_row(
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index),
            ),
            create_button(
                'Back',
                EMOJI_BACK,
                custom_id = _get_linked_quest_submission_back_direct_custom_id(
                    user_id,
                    page_index,
                    linked_quest_entry_id,
                    requirement_index,
                    item_page_index,
                    back_direct_location,
                ),
            ),
        ),
    ]


def build_linked_quest_submit_success_completed_components(
    client_id,
    user_id,
    page_index_quest_board,
    page_index_linked_quests,
    local_guild_id,
    linked_quest,
    quest_template,
    user_stats,
    user_level_old,
    submissions_normalised,
    rewards_normalised,
    executed_completion_count,
):
    """
    Builds successful item submission components when all the required items were submitted.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier who is rendering this message.
    
    user_id : `int`
        The invoking user's identifier.
    
    page_index_quest_board : `int`
        The quest board's current page's index.
    
    page_index_linked_quests : `int`
        The linked quests' current page's index.
    
    local_guild_id : `int`
        The local guild's identifier.
    
    linked_quest : : ``LinkedQuest``
        The finished quest.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    user_stats : ``UserStats``
        The user's stats.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    rewards_normalised : `None | list<(int, int, int)>`
        The rewards given by the quest in a normalised form.
    
    executed_completion_count : `int`
        How much times completion was executed.
    
    Returns
    -------
    components : ``list<Component>``
    """
    user_level_new = get_user_adventurer_rank_info(user_stats.credibility).level
    
    components = []
    
    # Description
    components.append(create_text_display(
        ''.join([*produce_linked_quest_submit_success_completed_description(
            client_id,
            submissions_normalised,
            rewards_normalised,
            executed_completion_count,
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
        
        if (quest_template.level > user_level_new + 1):
            repeat_enabled = False
            repeat_style = ButtonStyle.gray
            break
        
        repeat_enabled = True
        repeat_style = ButtonStyle.green
        break
    
    components.append(
        create_row(
            create_button(
                'View quest board',
                custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index_quest_board),
                enabled = (linked_quest.guild_id  == local_guild_id),
            ),
            create_button(
                'View my quests',
                custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER(user_id, page_index_linked_quests),
            ),
            create_button(
                'Repeat',
                custom_id = (
                    CUSTOM_ID_QUEST_ACCEPT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ACCEPT_BUILDER(user_id, linked_quest.guild_id, 0, quest_template.id)
                ),
                enabled = repeat_enabled,
                style = repeat_style,
            ),
        ),
    )
    
    return components


def build_quest_board_item_components(
    user_id, guild_id, page_index, quest_template_id, requirement_index, back_direct_location, item_id
):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The quest's source guild's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    
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
                'Back',
                EMOJI_BACK,
                custom_id = _get_quest_board_back_direct_custom_id(
                    user_id,
                    guild_id,
                    page_index,
                    quest_template_id,
                    requirement_index,
                    back_direct_location,
                ),
            ),
        ),
    ]


def build_quest_board_item_group_components(
    user_id, guild_id, page_index, quest_template_id, requirement_index, back_direct_location, item_group_id
):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The quest's source guild's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_nullable_item_group_description(get_item_group_nullable(item_group_id))])),
        create_separator(),
        create_row(
            create_button(
                'Back',
                EMOJI_BACK,
                custom_id = _get_quest_board_back_direct_custom_id(
                    user_id,
                    guild_id,
                    page_index,
                    quest_template_id,
                    requirement_index,
                    back_direct_location,
                ),
            ),
        ),
    ]


def build_linked_quest_item_components(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
    item_id,
):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    item_page_index : `int`
        The items' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
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
                'Back',
                EMOJI_BACK,
                custom_id = _get_linked_quest_submission_back_direct_custom_id(
                    user_id,
                    page_index,
                    linked_quest_entry_id,
                    requirement_index,
                    item_page_index,
                    back_direct_location,
                ),
            ),
        ),
    ]


def build_linked_quest_item_group_components(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
    item_group_id,
):
    """
    Builds components describing the given item group by identifier.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    item_page_index : `int`
        The items' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_nullable_item_group_description(get_item_group_nullable(item_group_id))])),
        create_separator(),
        create_row(
            create_button(
                'Back',
                EMOJI_BACK,
                custom_id = _get_linked_quest_submission_back_direct_custom_id(
                    user_id,
                    page_index,
                    linked_quest_entry_id,
                    requirement_index,
                    item_page_index,
                    back_direct_location,
                ),
            ),
        ),
    ]


def build_linked_quest_submit_select_requirement_components(
    linked_quest, inventory, page_index, requirement_select_page_index
):
    """
    Builds linked quest submission select requirement components.
    
    Parameters
    -----------
    linked_quest : ``LinkedQuest``
        Linked quest in context.
    
    inventory : ``Inventory``
        The user's inventory.
    
    page_index : `int`
        The page's index to back-direct to.
    
    requirement_select_page_index : `int`
        The requirement page index to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    submission_requirements_normalised = get_linked_quest_submission_requirements_normalised(linked_quest)
    if submission_requirements_normalised is None:
        submission_requirements_normalised_slice = None
    else:
        submission_requirements_normalised_slice = submission_requirements_normalised[
            requirement_select_page_index * REQUIREMENT_PAGE_SIZE :
            (requirement_select_page_index + 1) * REQUIREMENT_PAGE_SIZE
        ]
        if not submission_requirements_normalised_slice:
            submission_requirements_normalised_slice = None
    
    components = []
    
    # Header
    
    components.append(create_text_display(
        '### Select requirement to submit for'
    ))
    components.append(create_separator())
    
    # Requirement listing
    
    if (submission_requirements_normalised_slice is not None):
        for index, submission_requirement_normalised in enumerate(
            submission_requirements_normalised_slice, requirement_select_page_index * REQUIREMENT_PAGE_SIZE
        ):
            # Accumulate available
            accumulated_amount = 0
            accumulated_weight = 0
            accumulated_value = 0
            for item_entry in iter_submission_requirement_item_entries_of_normalised(
                inventory, submission_requirement_normalised
            ):
                amount = item_entry.amount
                item = item_entry.item
                
                accumulated_amount += amount
                accumulated_weight += amount * item.weight
                accumulated_value += amount * item.value
            
            components.append(create_text_display(
                ''.join([*produce_submission_requirements_entry_description(
                    submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
                )])
            ))
            
            if submission_requirement_normalised[4] >= submission_requirement_normalised[3]:
                submit_or_select_button_enabled = False
                submit_or_select_button_style = ButtonStyle.gray
            elif accumulated_amount:
                submit_or_select_button_enabled = True
                submit_or_select_button_style = ButtonStyle.green
            else:
                submit_or_select_button_enabled = False
                submit_or_select_button_style = ButtonStyle.green
                
            
            requirement_identifier = submission_requirement_normalised[1]
            requirement_type = submission_requirement_normalised[0]
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                button_submit = create_button(
                    'Submit items',
                    custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_BUILDER(
                        linked_quest.user_id, page_index, linked_quest.entry_id, index, requirement_identifier
                    ),
                    enabled = submit_or_select_button_enabled,
                    style = submit_or_select_button_style,
                )
            else:
                button_submit = create_button(
                    'Select item to submit',
                    custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER(
                        linked_quest.user_id, page_index, linked_quest.entry_id, index, 0,
                    ),
                    enabled = submit_or_select_button_enabled,
                    style = submit_or_select_button_style,
                )
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                button_information = create_button(
                    'Item information',
                    custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_REQUIREMENT_BUILDER(
                        linked_quest.user_id, page_index, linked_quest.entry_id, index, requirement_identifier
                    ),
                )
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
                button_information = create_button(
                    'Item group information',
                    custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_GROUP_REQUIREMENT_BUILDER(
                        linked_quest.user_id, page_index, linked_quest.entry_id, index, requirement_identifier
                    ),
                )
            
            else:
                button_information = None
            
            if button_information is None:
                row_component = create_row(
                    button_submit,
                )
            else:
                row_component = create_row(
                    button_submit,
                    button_information,
                )
            
            components.append(row_component)
            components.append(create_separator())
    
    # Control
    
    if submission_requirements_normalised is None:
        submission_requirement_normalised_count = 0
    else:
        submission_requirement_normalised_count = len(submission_requirements_normalised)
    
    if requirement_select_page_index == 0:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id, requirement_select_page_index - 1
        )
        enabled = True
    
    button_page_index_decrement = create_button(
        f'Page {requirement_select_page_index!s}',
        EMOJI_PAGE_PREVIOUS,
        custom_id = custom_id,
        enabled = enabled
    )
    
    if submission_requirement_normalised_count <= (requirement_select_page_index + 1) * REQUIREMENT_PAGE_SIZE:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id, requirement_select_page_index + 1
        )
        enabled = True
    
    button_page_index_increment = create_button(
        f'Page {requirement_select_page_index + 2!s}',
        EMOJI_PAGE_NEXT,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    components.append(create_row(
        button_page_index_decrement,
        button_page_index_increment,
        create_button(
            'Refresh',
            EMOJI_REFRESH,
            custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id, requirement_select_page_index
            ),
        ),
        create_button(
            'Back',
            EMOJI_BACK,
            custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id
            ),
        ),
    ))
    
    return components


def _iter_entry_by_name_sort_key_getter(item_entry):
    """
    Item entry key getter for sorting.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return item_entry.item.name


def build_linked_quest_submit_select_item_components(
    linked_quest, inventory, page_index, requirement_index, item_page_index, top,
):
    """
    Builds linked quest submission select requirement components.
    
    Parameters
    -----------
    linked_quest : ``LinkedQuest``
        Linked quest in context.
    
    inventory : ``Inventory``
        The user's inventory.
    
    page_index : `int`
        The page's index to back-direct to.
    
    requirement_index : `int`
        The requirement's page index to display.
    
    item_page_index : `int`
        The current local page index.
    
    top : `int`
        Whether to use top custom identifiers.
    
    Returns
    -------
    components : ``list<Component>``
    """
    submission_requirements_normalised = get_linked_quest_submission_requirements_normalised(linked_quest)
    if (submission_requirements_normalised is None) or (requirement_index >= len(submission_requirements_normalised)):
        submission_requirement_normalised = None
    else:
        submission_requirement_normalised = submission_requirements_normalised[requirement_index]
    
    if submission_requirement_normalised is None:
        item_entries = None
        item_entry_slice = None
    
    else:
        item_entries = [*iter_submission_requirement_item_entries_of_normalised(
            inventory, submission_requirement_normalised
        )]
        item_entries.sort(key = _iter_entry_by_name_sort_key_getter)
        
        item_entry_slice = item_entries[
            item_page_index * REQUIREMENT_PAGE_SIZE :
            (item_page_index + 1) * REQUIREMENT_PAGE_SIZE
        ]
        if not item_entry_slice:
            item_entry_slice = None
    
    # Accumulate available
    accumulated_amount = 0
    accumulated_weight = 0
    accumulated_value = 0
    
    if (item_entries is not None):
        for item_entry in item_entries:
            amount = item_entry.amount
            item = item_entry.item
            
            accumulated_amount += amount
            accumulated_weight += amount * item.weight
            accumulated_value += amount * item.value
    
    components = []
    
    # Header
    
    components.append(create_text_display(''.join([*produce_linked_quest_submission_item_select_header(
        submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
    )])))
    components.append(create_separator())
    
    # Item listing
    
    if (item_entry_slice is not None):
        for item_entry in item_entry_slice:
            components.append(create_text_display(
                ''.join([*produce_linked_quest_submission_item_select_description(
                    item_entry,
                    submission_requirement_normalised[2],
                )])
            ))
            
            if submission_requirement_normalised[4] >= submission_requirement_normalised[3]:
                submit_or_select_button_enabled = False
                submit_or_select_button_style = ButtonStyle.gray
            elif accumulated_amount:
                submit_or_select_button_enabled = True
                submit_or_select_button_style = ButtonStyle.green
            else:
                submit_or_select_button_enabled = False
                submit_or_select_button_style = ButtonStyle.green
            
            if top:
                custom_id_submit = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_BUILDER(
                    linked_quest.user_id,
                    page_index,
                    linked_quest.entry_id,
                    item_page_index,
                    item_entry.item.id,
                )
                custom_id_item_information = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_BUILDER(
                    linked_quest.user_id,
                    page_index,
                    linked_quest.entry_id,
                    item_page_index,
                    item_entry.item.id,
                )
            else:
                custom_id_submit = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_BUILDER(
                    linked_quest.user_id,
                    page_index,
                    linked_quest.entry_id,
                    requirement_index,
                    item_page_index,
                    item_entry.item.id,
                )
                custom_id_item_information = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_BUILDER(
                    linked_quest.user_id,
                    page_index,
                    linked_quest.entry_id,
                    requirement_index,
                    item_page_index,
                    item_entry.item.id,
                )
            
            components.append(create_row(
                create_button(
                    'Submit items',
                    custom_id = custom_id_submit,
                    enabled = submit_or_select_button_enabled,
                    style = submit_or_select_button_style,
                ),
                create_button(
                    'Item information',
                    custom_id = custom_id_item_information,
                ),
            ))
            components.append(create_separator())
    
    # Control
    
    if item_page_index == 0:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED
        enabled = False
    
    else:
        if top:
            custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id, item_page_index - 1
            )
        else:
            custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id, requirement_index, item_page_index - 1
            )
        enabled = True
    
    button_page_index_decrement = create_button(
        f'Page {item_page_index!s}',
        EMOJI_PAGE_PREVIOUS,
        custom_id = custom_id,
        enabled = enabled
    )
    
    if (0 if (item_entries is None) else len(item_entries)) <= (item_page_index + 1) * REQUIREMENT_PAGE_SIZE:
        custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED
        enabled = False
    
    else:
        if top:
            custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id, item_page_index + 1
            )
        else:
            custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER(
                linked_quest.user_id, page_index, linked_quest.entry_id, requirement_index, item_page_index + 1
            )
        enabled = True
    
    button_page_index_increment = create_button(
        f'Page {item_page_index + 2!s}',
        EMOJI_PAGE_NEXT,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    if top:
        refresh_custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id, item_page_index
        )
        back_custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id
        )
    else:
        refresh_custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id, requirement_index, item_page_index
        )
        back_custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER(
            linked_quest.user_id, page_index, linked_quest.entry_id, requirement_index // REQUIREMENT_PAGE_SIZE
        )
    
    components.append(create_row(
        button_page_index_decrement,
        button_page_index_increment,
        create_button(
            'Refresh',
            EMOJI_REFRESH,
            custom_id = refresh_custom_id,
        ),
        create_button(
            'Back',
            EMOJI_BACK,
            custom_id = back_custom_id,
        ),
    ))
    
    return components


def build_quest_select_requirement_components(
    user_id, guild_id, quest, inventory, page_index, requirement_select_page_index
):
    """
    Builds quest submission select requirement components.
    
    Parameters
    -----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The parent quest's guild's identifier.
    
    quest : ``Quest``
        Quest in context.
    
    inventory : ``Inventory``
        The user's inventory.
    
    page_index : `int`
        The page's index to back-direct to.
    
    requirement_select_page_index : `int`
        The requirement page index to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    submission_requirements_normalised = get_quest_submission_requirements_normalised(quest)
    if submission_requirements_normalised is None:
        submission_requirements_normalised_slice = None
    else:
        submission_requirements_normalised_slice = submission_requirements_normalised[
            requirement_select_page_index * REQUIREMENT_PAGE_SIZE :
            (requirement_select_page_index + 1) * REQUIREMENT_PAGE_SIZE
        ]
        if not submission_requirements_normalised_slice:
            submission_requirements_normalised_slice = None
    
    components = []
    
    # Header
    
    components.append(create_text_display(
        '### Select requirement to inspect'
    ))
    components.append(create_separator())
    
    # Requirement listing
    
    if (submission_requirements_normalised_slice is not None):
        for index, submission_requirement_normalised in enumerate(
            submission_requirements_normalised_slice, requirement_select_page_index * REQUIREMENT_PAGE_SIZE
        ):
            # Accumulate available
            accumulated_amount = 0
            accumulated_weight = 0
            accumulated_value = 0
            for item_entry in iter_submission_requirement_item_entries_of_normalised(
                inventory, submission_requirement_normalised
            ):
                amount = item_entry.amount
                item = item_entry.item
                
                accumulated_amount += amount
                accumulated_weight += amount * item.weight
                accumulated_value += amount * item.value
            
            components.append(create_text_display(
                ''.join([*produce_submission_requirements_entry_description(
                    submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
                )])
            ))
            
            requirement_identifier = submission_requirement_normalised[1]
            requirement_type = submission_requirement_normalised[0]
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                button_information = create_button(
                    'Item information',
                    custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_REQUIREMENT_BUILDER(
                        user_id, guild_id, page_index, quest.template_id, index, requirement_identifier
                    ),
                )
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
                button_information = create_button(
                    'Item group information',
                    custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_GROUP_REQUIREMENT_BUILDER(
                        user_id, guild_id, page_index, quest.template_id, index, requirement_identifier
                    ),
                )
            
            else:
                button_information = None
            
            if button_information is None:
                row_component = None
            else:
                row_component = create_row(
                    button_information,
                )
            
            if (row_component is not None):
                components.append(row_component)
            components.append(create_separator())
    
    # Control
    
    if submission_requirements_normalised is None:
        submission_requirement_normalised_count = 0
    else:
        submission_requirement_normalised_count = len(submission_requirements_normalised)
    
    if requirement_select_page_index == 0:
        custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_BUILDER(
            user_id, guild_id, page_index, quest.template_id, requirement_select_page_index - 1
        )
        enabled = True
    
    button_page_index_decrement = create_button(
        f'Page {requirement_select_page_index!s}',
        EMOJI_PAGE_PREVIOUS,
        custom_id = custom_id,
        enabled = enabled
    )
    
    if submission_requirement_normalised_count <= (requirement_select_page_index + 1) * REQUIREMENT_PAGE_SIZE:
        custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED
        enabled = False
    
    else:
        custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_BUILDER(
            user_id, guild_id, page_index, quest.template_id, requirement_select_page_index + 1
        )
        enabled = True
    
    button_page_index_increment = create_button(
        f'Page {requirement_select_page_index + 2!s}',
        EMOJI_PAGE_NEXT,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    components.append(create_row(
        button_page_index_decrement,
        button_page_index_increment,
        create_button(
            'Back',
            EMOJI_BACK,
            custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER(
                user_id, guild_id, page_index, quest.template_id
            ),
        ),
    ))
    
    return components


def build_quest_complete_confirmation_form(
    user_id, guild_id, page_index, quest, linked_quest, quest_template, user_stats, possession_count
):
    """
    Builds quest complete confirmation form.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    quest : ``Quest``
        The quest to describe.
    
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    user_stats : ``UserStats``
        The user's stats.
    
    possession_count : `int`
        How much times the required items are possessed by the user.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    components = []
    
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    
    # Description
    description = ''.join([*produce_quest_details_base_section(
        None, quest, quest_template, user_adventurer_rank_info.level
    )])
    if description:
        components.append(create_text_display(description))
    
    # Count input
    allowed_completion_count_string = str(get_allowed_completion_count(linked_quest, quest_template, possession_count))
    
    components.append(
        create_label(
            'How much times do you wish to complete it?',
            f'Up to {allowed_completion_count_string} times.',
            create_text_input(
                custom_id = CUSTOM_ID_COMPLETION_COUNT,
                placeholder = allowed_completion_count_string,
                required = False,
                max_length = len(allowed_completion_count_string),
                min_length = 1,
                value = allowed_completion_count_string,
            ),
        ),
    )
    
    # Build form
    return InteractionForm(
        'Please confirm completion',
        components,
        CUSTOM_ID_QUEST_BOARD_COMPLETE_BUILDER(user_id, guild_id, page_index, quest_template.id),
    )
