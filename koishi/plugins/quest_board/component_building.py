__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import (
    ButtonStyle, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ..item_core import get_item_nullable
from ..quest_core import (
    QUEST_TYPE_ITEM_SUBMISSION, get_guild_adventurer_rank_info, get_quest_template, get_user_adventurer_rank_info
)

from .constants import (
    BROKEN_QUEST_DESCRIPTION, CUSTOM_ID_LINKED_QUEST_ABANDON_FACTORY, CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_FACTORY, CUSTOM_ID_QUEST_ACCEPT_DISABLED, CUSTOM_ID_QUEST_ACCEPT_FACTORY,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY,
    CUSTOM_ID_QUEST_ITEM_DETAILS_DISABLED, CUSTOM_ID_QUEST_ITEM_DETAILS_FACTORY, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS,
    PAGE_SIZE
)
from .content_builders import (
    build_linked_quest_detailed_description, build_linked_quest_short_description,
    build_linked_quest_submit_success_completed_description, build_linked_quest_submit_success_n_left_description,
    build_linked_quest_header_description, build_nullable_item_description, build_quest_board_header_description,
    build_quest_detailed_description, build_quest_short_description
)


def build_quest_board_failure_guild_only_components():
    """
    Builds quest board components for the case when it is invoked from outside a guild.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('Only guilds have quest board.'),
    ]


def build_quest_board_quest_listing_components(guild, guild_stats, page_index):
    """
    Builds quest board quest listing.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    
    guild_stats : ``GuildStats``
        The guild's stats.
    
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
    
    header_content_component = create_text_display(build_quest_board_header_description(
        guild, guild_adventurer_rank_info, len(quest_batch.quests)),
    )
    
    icon_url = guild.icon_url
    if (icon_url is None):
        component = header_content_component
    else:
        component = create_section(header_content_component, thumbnail = create_thumbnail_media(icon_url))
    
    components.append(component)
    
    components.append(create_separator())
    
    # Add quests.
    quest_slice = quest_batch.quests[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    if quest_slice:
        for quest in quest_slice:
            quest_template = get_quest_template(quest.template_id)
            
            components.append(
                create_section(
                    create_text_display(
                        build_quest_short_description(quest, quest_template)
                    ),
                    thumbnail = create_button(
                        'Details',
                        custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY(quest_template.id),
                        enabled = (quest_template is not None),
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
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN(page_index - 1),
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
            custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN(page_index + 1),
        )
    
    components.append(create_row(button_page_index_decrement, button_page_index_increment))
    
    return components


def build_quest_details_components(quest, user_stats):
    """
    Builds quest details components describing a quest of a quest board with more details.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest to describe.
    
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
            build_quest_detailed_description(quest, quest_template, user_adventurer_rank_info.level),
        ),
    )
    components.append(create_separator())
    
    # Add interactive components.
    components.append(
        create_row(
            create_button(
                'Accept',
                custom_id = (
                    CUSTOM_ID_QUEST_ACCEPT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ACCEPT_FACTORY(quest_template.id)
                ),
                enabled = ((quest_template is not None) and (quest_template.level <= user_adventurer_rank_info.level)),
            ),
            create_button(
                'Item information',
                custom_id = (
                    CUSTOM_ID_QUEST_ITEM_DETAILS_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ITEM_DETAILS_FACTORY(quest_template.item_id)
                ),
                enabled = (quest_template is not None),
            ),
        ),
    )
    
    return components


def build_quest_failure_on_adventure_components():
    """
    Builds response components if the user is already on an adventure and therefore cannot accept a quest.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You cannot accept quests while adventuring.'),
    ]


def build_quest_failure_no_such_quest_components():
    """
    Builds response components when a quest is no longer available.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('This quest is no longer available.'),
    ]


def build_quest_accept_failure_quest_limit_components():
    """
    Builds response components when the user reached its quest imit and cannot accept more.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You cannot accept more quests.'),
    ]


def build_quest_accept_failure_duplicate_components():
    """
    Builds response components when the user already accepted the given quest.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You already have this quest currently accepted.'),
    ]


def build_quest_accept_failure_user_level_low_components():
    """
    Builds response components for the case when the user is too low level to accept the quest.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('Your rank is too low to accept this quest.'),
    ]


def build_quest_accept_success_components():
    """
    Builds response components when a quest is successfully accepted.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You successfully accepted the quest.'),
    ]


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
    components = []
    
    # Add header.
    user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
    components.append(
        create_section(
            create_text_display(build_linked_quest_header_description(
                user,
                guild_id,
                user_adventurer_rank_info,
                (0 if (linked_quest_listing is None) else len(linked_quest_listing)),
            )),
            thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
        ),
    )
    components.append(create_separator())
    
    # Add linked quests.
    if (linked_quest_listing is not None):
        linked_quest_slice = linked_quest_listing[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
        if linked_quest_slice:
            for linked_quest in linked_quest_slice:
                quest_template = get_quest_template(linked_quest.template_id)
                
                components.append(
                    create_section(
                        create_text_display(
                            build_linked_quest_short_description(linked_quest, quest_template)
                        ),
                        thumbnail = create_button(
                            'Details',
                            custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY(linked_quest.entry_id),
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
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN(page_index - 1),
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
            custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN(page_index + 1),
        )
    
    components.append(create_row(button_page_index_decrement, button_page_index_increment))
    
    return components


def build_linked_quest_details_components(linked_quest, user_stats):
    """
    Builds linked quest details components describing the accepted quest in details.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to describe.
    
    user_stats : ``UserStats``
        The user's stats.
    
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
            build_linked_quest_detailed_description(linked_quest, quest_template, user_adventurer_rank_info.level),
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
                'Submit items',
                custom_id = (
                    CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_LINKED_QUEST_SUBMIT_FACTORY(linked_quest.entry_id)
                ),
                enabled = submit_button_enabled,
                style = submit_button_style,
            ),
            create_button(
                'Abandon quest',
                custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_FACTORY(linked_quest.entry_id),
                style = abandon_quest_style,
            ),
            create_button(
                'Item information',
                custom_id = (
                    CUSTOM_ID_QUEST_ITEM_DETAILS_DISABLED
                    if quest_template is None else
                    CUSTOM_ID_QUEST_ITEM_DETAILS_FACTORY(quest_template.item_id)
                ),
                enabled = (quest_template is not None),
            ),
        ),
    )
    
    return components


def build_linked_quest_failure_on_adventure_components():
    """
    Builds response components for the case when the user cannot submit items due to being on an adventure.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You cannot submit items while on adventure.'),
    ]


def build_linked_quest_failure_no_such_quest_components():
    """
    Builds response components for the case when there is no such a linked quest available anymore.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You do not have such a quest.'),
    ]


def build_linked_quest_failure_expired_quest_components():
    """
    Builds response components for the case when a quest that is expires is interacted with.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('The quest expired, you cannot interact with it anymore.'),
    ]
    

def build_linked_quest_abandon_success_components():
    """
    Builds successfully abandoning response components.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You successfully accepted the quest.'),
    ]


def build_linked_quest_failure_broken_quest_components():
    """
    Builds response components when the a part of the quest is broken.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(BROKEN_QUEST_DESCRIPTION),
    ]


def build_linked_quest_submit_failure_no_items_to_submit_components():
    """
    Builds response components for the case when there are no items to submit.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You do not have any item to submit.'),
    ]


def build_linked_quest_submit_success_n_left_components(
    item, amount_type, amount_submitted, amount_required, amount_used
):
    """
    Builds successful item submission components when `n` items are still left to submit.
    
    Parameters
    ----------
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
            build_linked_quest_submit_success_n_left_description(
                item, amount_type, amount_submitted, amount_required, amount_used,
            ),
        ),
    ]


def build_linked_quest_submit_success_completed_components(
    item, amount_type, amount_required, amount_used, reward_balance, reward_credibility,
):
    """
    Builds successful item submission components when all the required items were submitted.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_balance : `int`
        The amount of balance the user receives.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            build_linked_quest_submit_success_completed_description(
                item, amount_type, amount_required, amount_used, reward_balance, reward_credibility,
            ),
        ),
    ]


def build_item_components(item_id):
    """
    Builds components describing the given item by identifier.
    
    Parameters
    ----------
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(build_nullable_item_description(get_item_nullable(item_id)))
    ]
