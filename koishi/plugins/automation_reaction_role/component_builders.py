__all__ = ()


from hata import (
    ButtonStyle, EMOJIS, EntitySelectDefaultValue, EntitySelectDefaultValueType, InteractionForm,
    StringSelectOption, create_button, create_label, create_role_select, create_row, create_section, create_separator,
    create_string_select, create_text_display
)

from .constants import (
    CONTENT_LENGTH_MAX, CONTENT_LENGTH_SPACE_SEARCH_AREA, CONTENT_LENGTH_TRUNCATE_AFTER, EMOJI_PAGE_DECREMENT,
    EMOJI_PAGE_INCREMENT, ENTRY_PAGE_SIZE, ITEMS_MAX
)
from .content_builders import get_emoji_name, produce_role_listing
from .custom_ids import (
    CUSTOM_ID_ADD_ROLES, CUSTOM_ID_EMOJI, CUSTOM_ID_ENTRY_DELETE_FACTORY, CUSTOM_ID_ENTRY_PAGE_VIEW_DECREMENT_DISABLED,
    CUSTOM_ID_ENTRY_PAGE_VIEW_FACTORY, CUSTOM_ID_ENTRY_PAGE_VIEW_INCREMENT_DISABLED, CUSTOM_ID_ITEM_ADD_FACTORY,
    CUSTOM_ID_ITEM_DELETE_FACTORY, CUSTOM_ID_ITEM_MODIFY_FACTORY, CUSTOM_ID_LISTING_PAGE_VIEW_DECREMENT_DISABLED,
    CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY, CUSTOM_ID_LISTING_PAGE_VIEW_INCREMENT_DISABLED, CUSTOM_ID_REMOVE_ROLES
)


def produce_short_content(message):
    """
    Produces a short content representing a message.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    message : ``Message``
        The message to represent.
    
    Yields
    ------
    part : `str`
    """
    total_length = 0
    for content in message.iter_contents():
        content_length = len(content)
        new_total_length = total_length + content_length
        
        if total_length:
            yield '\n\n'
        
        if new_total_length < CONTENT_LENGTH_MAX:
            yield content
            
            total_length = new_total_length
            if total_length > CONTENT_LENGTH_TRUNCATE_AFTER:
                break
            
            continue
        
        allowed_length_limit = CONTENT_LENGTH_MAX - total_length
        space_position = content.rfind(
            ' ',
            allowed_length_limit - CONTENT_LENGTH_SPACE_SEARCH_AREA,
            allowed_length_limit,
        )
        if space_position == -1:
            space_position = allowed_length_limit - 3
        
        yield content[:space_position]
        yield '...'
        break


def produce_roles_section(add_role_ids, remove_role_ids):
    """
    Produces a roles section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    add_role_ids : `None | tuple<int>`
        Role identifier to add upon reacting.
    
    remove_role_ids : `None | tuple<int>`
        Role identifiers to remove upon react.
    
    Yields
    ------
    part : `str`
    """
    if (add_role_ids is None) and (remove_role_ids is None):
        yield 'none'
        return
    
    if (add_role_ids is not None):
        yield 'Add roles:'
        yield from produce_role_listing(add_role_ids)
    
    if (remove_role_ids is not None):
        if (add_role_ids is not None):
            yield '\n'
        
        yield 'Remove roles:'
        yield from produce_role_listing(remove_role_ids)


def build_automation_reaction_role_listing_components(guild, automation_reaction_role_entries, listing_page_index):
    """
    Builds auto react roel listing components.
    
    Parameters
    ----------
    guild : ``Guild``
        The local guild.
    
    automation_reaction_role_entries : ``None | list<AutomationReactionRoleEntry>``
        Auto react role entries.
    
    listing_page_index : `int`
        The current listing page index.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # title
    components.append(create_text_display(f'### Auto react roles of {guild.name}'))
    
    components.append(create_separator())
    
    # pairs
    page_start = listing_page_index * ENTRY_PAGE_SIZE
    if (automation_reaction_role_entries is not None) and (len(automation_reaction_role_entries) > page_start):
        for automation_reaction_role_entry in automation_reaction_role_entries[
            page_start : page_start + ENTRY_PAGE_SIZE
        ]:
            content = ''.join([*produce_short_content(automation_reaction_role_entry.message)])
            
            components.append(
                create_section(
                    create_text_display(f'### {automation_reaction_role_entry.message.url}'),
                    *(
                        (create_text_display(content),) if content else () 
                    ),
                    thumbnail = create_button(
                        'View',
                        custom_id = CUSTOM_ID_ENTRY_PAGE_VIEW_FACTORY(
                            listing_page_index, automation_reaction_role_entry.message.id, 0
                        )
                    ),
                ),
            )
        components.append(create_separator())
    
    # control
    page_decrement_enabled = (listing_page_index > 0)
    page_increment_enabled = (
        (automation_reaction_role_entries is not None) and
        (len(automation_reaction_role_entries) > page_start + ENTRY_PAGE_SIZE)
    )
    
    components.append(
        create_row(
            create_button(
                f'Page {listing_page_index}',
                custom_id = (
                    CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY(
                        listing_page_index - 1
                    )
                    if page_decrement_enabled else
                    CUSTOM_ID_LISTING_PAGE_VIEW_DECREMENT_DISABLED
                    
                ),
                emoji = EMOJI_PAGE_DECREMENT,
                enabled = page_decrement_enabled,
            ),
            create_button(
                f'Page {listing_page_index + 2}',
                custom_id = (
                    CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY(
                        listing_page_index + 1
                    )
                    if page_increment_enabled else
                    CUSTOM_ID_LISTING_PAGE_VIEW_INCREMENT_DISABLED
                ),
                enabled = page_increment_enabled,
                emoji = EMOJI_PAGE_INCREMENT,
            ),
        )
    )
    
    return components


def build_automation_reaction_role_entry_delete_form(listing_page_index, automation_reaction_role_entry):
    """
    Builds a confirmation form for deleting a whole entry.
    
    Parameters
    ----------
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    return InteractionForm(
        'Please confirm your deletion',
        [
            create_text_display('-# _ _')
        ],
        custom_id = CUSTOM_ID_ENTRY_DELETE_FACTORY(listing_page_index, automation_reaction_role_entry.message.id),
    )


def build_automation_reaction_role_entry_overview_components(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index
):
    """
    Builds auto react role overview components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    overview_page_index : `int`
        The current overview page index.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # title
    components.append(create_text_display(f'### Auto react role {automation_reaction_role_entry.message.url}'))
    
    # content
    content = ''.join([*produce_short_content(automation_reaction_role_entry.message)])
    if content:
        components.append(create_text_display(content))
    
    components.append(create_separator())
    
    # items
    items = automation_reaction_role_entry.items
    page_start = overview_page_index * ENTRY_PAGE_SIZE
    if (items is not None) and (len(items) > page_start):
        for item in items[page_start : page_start + ENTRY_PAGE_SIZE]:
            components.append(
                create_section(
                    create_text_display(get_emoji_name(user, item.emoji_id)),
                    create_text_display(''.join([*produce_roles_section(item.add_role_ids, item.remove_role_ids)])),
                    thumbnail = create_button(
                        'Modify',
                        custom_id = CUSTOM_ID_ITEM_MODIFY_FACTORY(
                            listing_page_index,
                            automation_reaction_role_entry.message.id,
                            overview_page_index,
                            item.emoji_id,
                        ),
                    ),
                ),
            )
        
        components.append(create_separator())
    
    # control
    page_decrement_enabled = (overview_page_index > 0)
    page_increment_enabled = (items is not None) and (len(items) > page_start + ENTRY_PAGE_SIZE)
    add_new_enabled = (items is None) or (len(items) < ITEMS_MAX)
    
    components.append(
        create_row(
            create_button(
                f'Page {overview_page_index}',
                custom_id = (
                    CUSTOM_ID_ENTRY_PAGE_VIEW_FACTORY(
                        listing_page_index, automation_reaction_role_entry.message.id, overview_page_index - 1
                    )
                    if page_decrement_enabled else
                    CUSTOM_ID_ENTRY_PAGE_VIEW_DECREMENT_DISABLED
                ),
                emoji = EMOJI_PAGE_DECREMENT,
                enabled = page_decrement_enabled,
            ),
            create_button(
                f'Page {overview_page_index + 2}',
                custom_id = (
                    CUSTOM_ID_ENTRY_PAGE_VIEW_FACTORY(
                        listing_page_index, automation_reaction_role_entry.message.id, overview_page_index + 1
                    )
                    if page_increment_enabled else
                    CUSTOM_ID_ENTRY_PAGE_VIEW_INCREMENT_DISABLED
                ),
                enabled = page_increment_enabled,
                emoji = EMOJI_PAGE_INCREMENT,
            ),
            create_button(
                'Back to listing',
                custom_id = CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY(listing_page_index),
            ),
            create_button(
                'Delete',
                custom_id = CUSTOM_ID_ENTRY_DELETE_FACTORY(
                    listing_page_index, automation_reaction_role_entry.message.id
                ),
                style = ButtonStyle.red,
            ),
        )
    )
    components.append(
        create_row(
            create_button(
                'Add new',
                custom_id = CUSTOM_ID_ITEM_ADD_FACTORY(listing_page_index, automation_reaction_role_entry.message.id),
                enabled = add_new_enabled,
                style = ButtonStyle.green,
            ),
            create_button(
                'Delete one',
                custom_id = CUSTOM_ID_ITEM_DELETE_FACTORY(
                    listing_page_index, automation_reaction_role_entry.message.id, overview_page_index
                ),
                enabled = (items is not None),
            ),
            # create_button(
            #     'Sync',
            #     custom_id = (
            #         CUSTOM_ID_ENTRY_SYNC_FACTORY(listing_page_index, automation_reaction_role_entry.message.id
            #     ),
            # ),
        ),
    )
    
    return components


def build_automation_reaction_role_entry_overview_deleted_components(listing_page_index):
    """
    Builds auto react role overview deleted components.
    
    Parameters
    ----------
    listing_page_index : `int`
        The current listing page index.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # title
    components.append(create_text_display('### Auto react role not found'))
    components.append(create_separator())
    
    # control
    components.append(
        create_row(
            create_button(
                'Back to listing',
                custom_id = CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY(listing_page_index),
            ),
        )
    )
    
    return components


def build_automation_reaction_role_item_add_form(user, listing_page_index, automation_reaction_role_entry):
    """
    Builds add form for adding a new reaction.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    # Produce emoji choices as available.
    emoji_choices = []
    
    reactions = automation_reaction_role_entry.message.reactions
    if (reactions is not None) and reactions:
        exhausted_emoji_ids = set()
        
        automation_reaction_role_items = automation_reaction_role_entry.items
        if (automation_reaction_role_items is not None):
            for automation_reaction_role_item in automation_reaction_role_items:
                exhausted_emoji_ids.add(automation_reaction_role_item.emoji_id)
        
        for reaction in reactions.iter_reactions():
            emoji = reaction.emoji
            emoji_id = emoji.id
            if emoji_id in exhausted_emoji_ids:
                continue
            
            exhausted_emoji_ids.add(emoji_id)
            emoji_choices.append(StringSelectOption(
                format(emoji_id, 'x'),
                emoji.name,
                (emoji if user.can_use_emoji(emoji) else None),
                default = (False if emoji_choices else True),
            ))
    
    if not emoji_choices:
        emoji_choices.append(StringSelectOption(
            '0',
            'none',
            default = True,
        ))
    
    # Build the form.
    return InteractionForm(
        'Add new emoji',
        [
            create_label(
                'Emoji',
                component = create_string_select(
                    emoji_choices,
                    custom_id = CUSTOM_ID_EMOJI,
                ),
            ),
            create_label(
                'Added roles upon reacting',
                component = create_role_select(
                    custom_id = CUSTOM_ID_ADD_ROLES,
                    max_values = 25,
                    min_values = 0,
                ),
            ),
            create_label(
                'Removed roles upon reacting',
                component = create_role_select(
                    custom_id = CUSTOM_ID_REMOVE_ROLES,
                    max_values = 25,
                    min_values = 0,
                ),
            ),
        ],
        custom_id = CUSTOM_ID_ITEM_ADD_FACTORY(listing_page_index, automation_reaction_role_entry.message.id),
    )


def build_automation_reaction_role_item_modify_form(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index, item
):
    """
    Builds add form for modifying a reaction.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    overview_page_index : `int`
        The overview's page index to redirect back to.
    
    item : ``AutoreactRoleItem``
        The item to prompt modification form for.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    add_role_ids = item.add_role_ids
    remove_role_ids = item.remove_role_ids
    
    return InteractionForm(
        'Modify emoji',
        [
            create_text_display(get_emoji_name(user, item.emoji_id)),
            create_label(
                'Added roles upon reacting',
                component = create_role_select(
                    custom_id = CUSTOM_ID_ADD_ROLES,
                    default_values = (
                        None
                        if add_role_ids is None else
                        [
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id)
                            for role_id in add_role_ids
                        ]
                    ),
                    max_values = 25,
                    min_values = 0,
                ),
            ),
            create_label(
                'Removed roles upon reacting',
                component = create_role_select(
                    custom_id = CUSTOM_ID_REMOVE_ROLES,
                    default_values = (
                        None
                        if remove_role_ids is None else
                        [
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id)
                            for role_id in remove_role_ids
                        ]
                    ),
                    max_values = 25,
                    min_values = 0,
                ),
            ),
        ],
        custom_id = CUSTOM_ID_ITEM_MODIFY_FACTORY(
            listing_page_index, automation_reaction_role_entry.message.id, overview_page_index, item.emoji_id
        ),
    )


def build_automation_reaction_role_item_delete_form(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index
):
    """
    Builds add form for modifying a reaction.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    overview_page_index : `int`
        The overview's page index to redirect back to.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    emoji_choices = []
    automation_reaction_role_items = automation_reaction_role_entry.items
    if automation_reaction_role_items is None:
        emoji_choices.append(StringSelectOption(
            '0',
            'none',
            default = True,
        ))
    else:
        for automation_reaction_role_item in automation_reaction_role_items:
            emoji_id = automation_reaction_role_item.emoji_id
            emoji = EMOJIS.get(emoji_id, None)
            
            emoji_choices.append(StringSelectOption(
                format(emoji_id, 'x'),
                (str(emoji_id) if emoji is None else emoji.name),
                (emoji if ((emoji is not None) and user.can_use_emoji(emoji)) else None),
            ))
    
    return InteractionForm(
        'Delete emoji',
        [
            create_label(
                'Emoji',
                component = create_string_select(
                    emoji_choices,
                    custom_id = CUSTOM_ID_EMOJI,
                ),
            )
        ],
        custom_id = CUSTOM_ID_ITEM_DELETE_FACTORY(
            listing_page_index, automation_reaction_role_entry.message.id, overview_page_index
        ),
    )
