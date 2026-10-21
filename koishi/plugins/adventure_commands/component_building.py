__all__ = ()

from itertools import islice

from hata import (
    InteractionForm, StringSelectOption, create_button, create_label, create_row, create_section, create_separator,
    create_string_select, create_text_display, create_thumbnail_media, format_unix_time
)

from ..adventure_core import (
    ADVENTURE_STATE_FINALISED, adventure_action_group_loot_by_state, adventure_action_listing_group_loot_by_state,
    can_cancel_adventure_after, can_cancel_adventure_any, can_cancel_adventure_now
)
from ..item_core import butcher_estimate_energy_cost, butcher_estimate_loot_chance_and_amounts
from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_ACTION_DISABLE

from .constants import (
    ACTIVE_ADVENTURE_ACTION_LIMIT, ADVENTURE_ACTION_LISTING_PAGE_SIZE, ADVENTURE_CANCELLATION_MODE_AFTER,
    ADVENTURE_CANCELLATION_MODE_NOW, ADVENTURE_LOOT_LISTING_MODE_DEFAULT, ADVENTURE_LOOT_LISTING_MODE_THIS_STEP,
    ADVENTURE_LOOT_LISTING_MODE_TOTAL, ADVENTURE_VIEW_MODE_DEFAULT, ADVENTURE_VIEW_MODE_DETAILED, EMOJI_REFRESH
)
from .content_building import (
    produce_adventure_action_listing_view_header, produce_adventure_action_notification_header,
    produce_adventure_action_short_representation, produce_adventure_action_view_description,
    produce_adventure_action_view_header, produce_adventure_cancellation_confirmation_description,
    produce_adventure_initial_representation, produce_adventure_listing_view_header,
    produce_adventure_return_notification_description, produce_adventure_return_notification_header,
    produce_adventure_short_representation, produce_adventure_view_description,
    produce_adventure_view_description_detailed_listing, produce_adventure_view_header,
    produce_butcher_done_description, produce_butcher_header, produce_butcher_item_description,
    produce_butcher_recovering_until_footer, produce_butcher_step_description, produce_loot_listing
)
from .custom_ids import (
    CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER, CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_BUILDER, CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN, CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_BUILDER,
    CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_BUILDER, CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_BUILDER,
    CUSTOM_ID_ADVENTURE_CANCELLATION_MODE, CUSTOM_ID_ADVENTURE_CANCEL_BUILDER,
    CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_BUILDER, CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER,
    CUSTOM_ID_ADVENTURE_VIEW_BUILDER
)


def build_adventure_create_confirmation_form(
    user_id, location, target, duration, return_, auto_cancellation, goal
):
    """
    Builds adventure create confirmation components.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    location : ``Location``
        Target duration.
    
    target : ``Target``
        Target action set.
    
    duration : `int`
        Duration.
    
    return_ : ``Return``
        Return logic identifier.
    
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    goal : ``None | Goal``
        The goal of the adventure.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    return InteractionForm(
        'Confirm your adventure',
        [
            create_text_display(''.join([*
                produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation, goal),
            ])),
        ],
        CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_BUILDER(
            user_id, location.id, target.id, duration, return_.id, auto_cancellation.id, goal
        ),
    )


def build_adventure_create_confirm_components(
    user_id, adventure_entry_id, location, target, duration, return_, auto_cancellation, goal
):
    """
    Builds adventure create approval components.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    adventure_entry_id : `int`
        The adventure's entries identifier in the database.
    
    location : ``Location``
        Target duration.
    
    target : ``Target``
        Target action set.
    
    duration : `int`
        Duration.
    
    return_ : ``Return``
        Return logic identifier.
    
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    goal : ``None | Goal``
        The goal of the adventure.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('### You began your adventure, best of luck brave adventurer!'),
        create_separator(),
        create_text_display(''.join([*
            produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation, goal),
        ])),
        create_separator(),
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    user_id,
                    adventure_entry_id,
                    ADVENTURE_VIEW_MODE_DEFAULT,
                    False,
                    0,
                ),
            ),
        ),
    ]


def build_adventure_cancellation_confirmation_form(adventure):
    """
    Builds adventure cancellation confirmation form.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to build for.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    components = [
        create_text_display(''.join([*produce_adventure_cancellation_confirmation_description(adventure)]))
    ]
    
    # If the adventure can be cancelled both after the next action and now,
    # allow the user to chose between the two options.
    if can_cancel_adventure_after(adventure) and can_cancel_adventure_now(adventure):
        components.append(create_label(
            'Cancellation mode',
            'Do you want to cancel the adventure immediately or only after the next action if finished?',
            create_string_select(
                [
                    StringSelectOption(format(ADVENTURE_CANCELLATION_MODE_NOW, 'x'), 'Immediately', default = True),
                    StringSelectOption(format(ADVENTURE_CANCELLATION_MODE_AFTER, 'x'), 'After'),
                ],
                custom_id = CUSTOM_ID_ADVENTURE_CANCELLATION_MODE,
            ),
        ))
    
    return InteractionForm(
        'Confirm adventure cancellation',
        components,
        CUSTOM_ID_ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
    )


def build_adventure_cancellation_components(cancellation_mode):
    """
    Builds adventure successful cancellation components.
    
    Parameters
    ----------
    cancellation_mode : `int`
        How the adventure was cancelled.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if cancellation_mode == ADVENTURE_CANCELLATION_MODE_NOW:
        next_action_description = 'You head back home immediately.'
    else:
        next_action_description = 'You will head back after the next action is completed.'
    
    return [
        create_text_display('You successfully cancelled your adventure.'),
        create_text_display(next_action_description),
    ]


def iter_build_adventure_action_components(
    adventure,
    adventure_action_listing_start,
    adventure_action_listing_end,
    produce_depart,
    produce_return,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    allow_switching_to_adventure_action_listing_view,
    adventure_action_listing_page_index,
):
    """
    Iterates over built adventure actions components.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_action_listing_start : `int`
        Where to start listing the actions (inclusive).
    
    adventure_action_listing_end : `int`
        Where to end listing the actions (exclusive).
    
    produce_depart : `bool`
        Whether to produce depart component.
    
    produce_return : `bool`
        Whether to produce return component.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    allow_switching_to_adventure_action_listing_view : `bool`
        Whether switching to adventure action listing view is allowed from a action view.
    
    adventure_action_listing_page_index : `int`
        Adventure action listing page index to direct to from adventure action view.
    
    Yields
    ------
    component : ``Component``
    """
    if produce_depart:
        yield create_section(
            create_text_display(
                f'{format_unix_time(adventure.created_at, "T")} Depart'
            ),
            thumbnail = create_button(
                'View',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART,
                enabled = False,
            ),
        )
    
    adventure_action_listing = adventure.action_listing
    if (adventure_action_listing is not None):
        for index in range(adventure_action_listing_start, adventure_action_listing_end):
            adventure_action = adventure_action_listing[index]
            text_display = create_text_display(
                ''.join([*produce_adventure_action_short_representation(adventure_action)])
            )
            
            yield create_section(
                text_display,
                thumbnail = create_button(
                    'View',
                    custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_BUILDER(
                        adventure.user_id,
                        adventure.entry_id,
                        index,
                        adventure_view_mode,
                        allow_switching_to_adventure_listing_view,
                        adventure_listing_page_index,
                        allow_switching_to_adventure_action_listing_view,
                        adventure_action_listing_page_index,
                    ),
                    enabled = (
                        (adventure_action.battle_data is not None) or
                        (adventure_action.loot_data is not None) or
                        (True if adventure_action.health_exhausted else False) or
                        (True if adventure_action.energy_exhausted else False)
                    ),
                )
            )
    
    if produce_return:
        yield create_section(
            create_text_display(
                f'{format_unix_time(adventure.updated_at, "T")} Return'
            ),
            thumbnail = create_button(
                'View',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN,
                enabled = False,
            ),
        )


def _build_adventure_finalised_control_components(
    adventure,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
):
    """
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to build for.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    Returns
    -------
    component : ``Component``
    """
    finalised = adventure.state == ADVENTURE_STATE_FINALISED
    
    component_refresh = create_button(
        'Refresh',
        EMOJI_REFRESH,
        enabled = (not finalised),
        custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
            adventure.user_id,
            adventure.entry_id,
            adventure_view_mode,
            allow_switching_to_adventure_listing_view,
            adventure_listing_page_index,
        ),
    )
    
    component_view_adventure_listing = create_button(
        'Back to adventures',
        enabled = allow_switching_to_adventure_listing_view,
        custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER(
            adventure.user_id,
            adventure_listing_page_index,
        ),
    )
    
    if finalised:
        view_action_listing_enable = True
    else:
        adventure_action_listing = adventure.action_listing
        if (adventure_action_listing is None):
            view_action_listing_enable = False
        else:
            view_action_listing_enable = len(adventure_action_listing) >= ACTIVE_ADVENTURE_ACTION_LIMIT
    
    component_view_action_listing = create_button(
        'View all action',
        enabled = view_action_listing_enable,
        custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
            adventure.user_id,
            adventure.entry_id,
            adventure_view_mode,
            allow_switching_to_adventure_listing_view,
            adventure_listing_page_index,
            0,
        ),
    )
    
    if finalised:
        cancel_enabled = False
    else:
        cancel_enabled = can_cancel_adventure_any(adventure)
    
    component_cancel = create_button(
        'Cancel',
        enabled = cancel_enabled,
        custom_id = CUSTOM_ID_ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
    )
    
    while True:
        if adventure_view_mode != ADVENTURE_VIEW_MODE_DEFAULT:
            if adventure_view_mode == ADVENTURE_VIEW_MODE_DETAILED:
                component = create_row(
                    component_refresh,
                    component_view_adventure_listing,
                    component_view_action_listing,
                    component_cancel,
                )
                break
        
        component = create_row(
            component_refresh,
            component_view_adventure_listing,
            component_view_action_listing,
            component_cancel,
            create_button(
                'Detailed',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    ADVENTURE_VIEW_MODE_DETAILED,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
        )
        break
    
    return component


def build_adventure_view_components(
    adventure,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    inventory_total,
    inventory_exhausted,
):
    """
    Builds components for an active adventure describing it.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ---
    
    components.append(
        create_text_display(''.join([*produce_adventure_view_header(adventure)])),
    )
    
    components.append(create_separator())
    
    # ---- Description ---
    
    while True:
        if adventure_view_mode != ADVENTURE_VIEW_MODE_DEFAULT:
            if adventure_view_mode == ADVENTURE_VIEW_MODE_DETAILED:
                producer_function = produce_adventure_view_description_detailed_listing
                break
            
            # No other cases
        
        producer_function = produce_adventure_view_description
        break
    
    components.append(create_text_display(
        ''.join([*producer_function(adventure, inventory_total, inventory_exhausted)])
    ),)
    
    components.append(create_separator())
    
    # ---- Loot ----
    
    adventure_action_listing = adventure.action_listing
    if (
        (adventure_action_listing is not None) and
        any((adventure_action.loot_data is not None) for adventure_action in adventure_action_listing)
    ):
        loot_by_state = adventure_action_listing_group_loot_by_state(adventure_action_listing)
    
        if (adventure_view_mode != ADVENTURE_VIEW_MODE_DETAILED) or (adventure.state == ADVENTURE_STATE_FINALISED):
            components.append(create_text_display(''.join([*produce_loot_listing(
                loot_by_state, ADVENTURE_LOOT_LISTING_MODE_DEFAULT,
            )])))
        
        else:
            adventure_action_latest = adventure_action_listing[-1]
            if (adventure_action_latest.loot_data is not None):
                
                components.append(create_text_display(''.join([*produce_loot_listing(
                    adventure_action_group_loot_by_state(adventure_action_latest),
                    ADVENTURE_LOOT_LISTING_MODE_THIS_STEP,
                )])))
                components.append(create_separator())
            
            components.append(create_text_display(''.join([*produce_loot_listing(
                loot_by_state, ADVENTURE_LOOT_LISTING_MODE_TOTAL,
            )])))
        
        components.append(create_separator())
    
    # ---- Adventure actions ----
    
    if adventure.state != ADVENTURE_STATE_FINALISED:
        if (adventure_action_listing is None):
            produce_depart = True
            adventure_action_listing_start = 0
            adventure_action_listing_end = 0
        else:
            adventure_action_listing_length = len(adventure_action_listing)
            if adventure_action_listing_length < ACTIVE_ADVENTURE_ACTION_LIMIT:
                produce_depart = True
                adventure_action_listing_start = 0
                adventure_action_listing_end = len(adventure_action_listing)
            else:
                produce_depart = False
                adventure_action_listing_start = adventure_action_listing_length - ACTIVE_ADVENTURE_ACTION_LIMIT
                adventure_action_listing_end = adventure_action_listing_length
                
                truncated_count = adventure_action_listing_length + 1 - ACTIVE_ADVENTURE_ACTION_LIMIT
                if truncated_count:
                    components.append(
                        create_text_display(
                            f'+ {truncated_count} truncated (showing latest {ACTIVE_ADVENTURE_ACTION_LIMIT})'
                    )
                )
        
        components.extend(
            iter_build_adventure_action_components(
                adventure,
                adventure_action_listing_start,
                adventure_action_listing_end,
                produce_depart,
                False,
                adventure_view_mode,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
                False,
                0,
            )
        )
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(_build_adventure_finalised_control_components(
        adventure,
        adventure_view_mode,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
    ))
    
    return components


def build_adventure_action_view_components(
    user_id,
    adventure_entry_id,
    adventure_action,
    adventure_action_index,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    allow_switching_to_adventure_action_listing_view,
    adventure_action_listing_page_index,
):
    """
    Builds components showing adventure actions.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    adventure_entry_id : `int`
        The owner adventure's identifier.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    adventure_action_index : `int`
        The adventure action's index.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    allow_switching_to_adventure_action_listing_view : `bool`
        Whether switching to action listing view is allowed from a action view.
    
    adventure_action_listing_page_index : `int`
        Adventure action listing page index to direct to from action view.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ----
    
    components.append(
        create_text_display(''.join([*produce_adventure_action_view_header(adventure_action)]))
    )
    components.append(create_separator())
    
    # ---- Description ----
    
    components.append(
        create_text_display(''.join([*produce_adventure_action_view_description(adventure_action)]))
    )
    components.append(create_separator())
    
    # ---- Battle ----
    
    # Battles are not implemented yet.
    
    # ---- Loot ----
    
    if (adventure_action.loot_data is not None):
        components.append(
            create_text_display(''.join([*produce_loot_listing(
                adventure_action_group_loot_by_state(adventure_action),
                ADVENTURE_LOOT_LISTING_MODE_DEFAULT,
            )])),
        )
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    user_id,
                    adventure_entry_id,
                    adventure_view_mode,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to actions',
                enabled = allow_switching_to_adventure_action_listing_view,
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    user_id,
                    adventure_entry_id,
                    adventure_view_mode,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    adventure_action_listing_page_index,
                ),
            ),
            create_button(
                'View battle logs',
                enabled = False, # Battles are not implemented yet.
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER(
                    user_id, adventure_entry_id, adventure_action_index
                ),
            ),
        )
    )
    
    return components


def build_adventure_action_listing_view_components(
    adventure,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    adventure_action_listing_page_index,
):
    """
    Builds adventure action listing view components.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    adventure_action_listing_page_index : `int`
        The page index to show.
    
    Returns
    -------
    components : ``list<Component>``
    """
    adventure_finalised = (adventure.state == ADVENTURE_STATE_FINALISED)
    
    adventure_action_listing = adventure.action_listing
    action_count = (0 if adventure_action_listing is None else len(adventure_action_listing)) + 1 + adventure_finalised
    page_count = (action_count + ADVENTURE_ACTION_LISTING_PAGE_SIZE - 1) // ADVENTURE_ACTION_LISTING_PAGE_SIZE
    
    components = []
    
    # ---- Header ----
    
    components.append(
        create_text_display(''.join([*
            produce_adventure_action_listing_view_header(adventure, adventure_action_listing_page_index)
        ]))
    )
    components.append(create_separator())
    
    # ---- Adventure action listing ----
    
    if (adventure_action_listing_page_index > -1) and (adventure_action_listing_page_index < page_count):
        produce_depart = (adventure_action_listing_page_index == 0)
        produce_return = adventure_finalised and (page_count - adventure_action_listing_page_index == 1)
        
        if adventure_action_listing is None:
            adventure_action_listing_start = 0
            adventure_action_listing_end = 0
        else:
            adventure_listing_length = len(adventure_action_listing)
            adventure_action_listing_start = adventure_action_listing_page_index * ADVENTURE_ACTION_LISTING_PAGE_SIZE - 1
            if adventure_action_listing_start < 0:
                adventure_action_listing_start = 0
            
            if adventure_action_listing_start >= adventure_listing_length:
                adventure_action_listing_start = 0
                adventure_action_listing_end = 0
            else:
                adventure_action_listing_end = (
                    (adventure_action_listing_page_index + 1) * ADVENTURE_ACTION_LISTING_PAGE_SIZE - 1
                )
                if adventure_action_listing_end > adventure_listing_length:
                    adventure_action_listing_end = adventure_listing_length

        
        components.extend(
            iter_build_adventure_action_components(
                adventure,
                adventure_action_listing_start,
                adventure_action_listing_end,
                produce_depart,
                produce_return,
                adventure_view_mode,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
                True,
                adventure_action_listing_page_index,
            )
        )
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    adventure_view_mode,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                f'Page {adventure_action_listing_page_index}',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    adventure_view_mode,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    max(0, adventure_action_listing_page_index - 1),
                ),
                enabled = (adventure_action_listing_page_index > 0),
            ),
            create_button(
                f'Page {adventure_action_listing_page_index + 2}',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    adventure_view_mode,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    adventure_action_listing_page_index + 1,
                ),
                enabled = (adventure_action_listing_page_index < (page_count - 1)),
            ),
        )
    )
    
    return components


def build_adventure_listing_view_components(user_id, adventure_listing, adventure_listing_page_index, page_count):
    """
    Builds action listing view components.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    adventure_listing : ``None | list<Adventure>``
        Adventures to display.
    
    adventure_listing_page_index : `int`
        The shown page's index,
    
    page_count : `int`
        The amount of pages.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ----
    
    components.append(
        create_text_display(''.join([*produce_adventure_listing_view_header(adventure_listing_page_index)]))
    )
    components.append(create_separator())
    
    # ---- Adventure listing ----
    
    if (adventure_listing is not None):
        for adventure in adventure_listing:
            components.append(
                create_section(
                    create_text_display(''.join([*produce_adventure_short_representation(adventure)])),
                    thumbnail = create_button(
                        'View',
                        custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                            user_id,
                            adventure.entry_id,
                            ADVENTURE_VIEW_MODE_DEFAULT,
                            True,
                            adventure_listing_page_index,
                        ),
                    ),
                ),
            )
        
        components.append(create_separator())
    
    # ---- control ----
    
    components.append(
        create_row(
            create_button(
                f'Page {adventure_listing_page_index}',
                custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER(
                    user_id, max(0, adventure_listing_page_index - 1),
                ),
                enabled = (adventure_listing_page_index > 0),
            ),
            create_button(
                f'Page {adventure_listing_page_index + 2}',
                custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER(
                    user_id, adventure_listing_page_index + 1,
                ),
                enabled = (adventure_listing_page_index < (page_count - 1)),
            ),
        )
    )
    
    return components


def build_adventure_return_notification_components(adventure):
    """
    Builds adventure return notification components.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user returned from.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ----
    
    components.append(
        create_text_display(''.join([*produce_adventure_return_notification_header(adventure)])),
    )
    
    components.append(create_separator()
    )
    
    # ---- description ----
    
    if adventure.health_exhausted or adventure.energy_exhausted:
        components.append(
            create_text_display(''.join([*produce_adventure_return_notification_description(adventure)])),
        )
        components.append(create_separator())
    
    # ---- Loot ----
    
    adventure_action_listing = adventure.action_listing
    if (
        (adventure_action_listing is not None) and
        any((adventure_action.loot_data is not None) for adventure_action in adventure_action_listing)
    ):
        components.append(create_text_display(''.join([*produce_loot_listing(
            adventure_action_listing_group_loot_by_state(adventure_action_listing),
            ADVENTURE_LOOT_LISTING_MODE_DEFAULT,
        )])))
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(_build_adventure_finalised_control_components(adventure, ADVENTURE_VIEW_MODE_DEFAULT, False, 0))
    
    return components


def build_adventure_action_notification_components(adventure, adventure_action):
    """
    Builds components showing adventure actions.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user is on.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ----
    
    components.append(
        create_text_display(''.join([*produce_adventure_action_notification_header(adventure, adventure_action)]))
    )
    components.append(create_separator())
    
    # ---- Battle ----
    
    # Battles are not implemented yet.
    
    # ---- Loot ----
    
    if (adventure_action.loot_data is not None):
        components.append(
            create_text_display(''.join([*produce_loot_listing(
                adventure_action_group_loot_by_state(adventure_action),
                ADVENTURE_LOOT_LISTING_MODE_THIS_STEP,
            )])),
        )
        components.append(create_separator())
        
        components.append(create_text_display(''.join([*produce_loot_listing(
            adventure_action_listing_group_loot_by_state(adventure.action_listing),
            ADVENTURE_LOOT_LISTING_MODE_TOTAL,
        )])))
        components.append(create_separator())
    
    # ---- Controls ----
    
    # Detect which index this adventure action is at.
    adventure_action_listing = adventure.action_listing
    if (adventure_action_listing is None):
        adventure_action_index = 0
    else:
        for adventure_action_index in range(len(adventure_action_listing) -1, -1, -1):
            if adventure_action_listing[adventure_action_index] is adventure_action:
                break
        else:
            # This is not required, but calms the editor.
            adventure_action_index = 0
            
    components.append(
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id, adventure.entry_id, ADVENTURE_VIEW_MODE_DEFAULT, False, 0,
                ),
            ),
            create_button(
                'View adventure (detailed)',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id, adventure.entry_id, ADVENTURE_VIEW_MODE_DETAILED, False, 0,
                ),
            ),
            create_button(
                'View battle logs',
                enabled = False, # Battles are not implemented yet.
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER(
                    adventure.user_id, adventure.entry_id, adventure_action_index
                ),
            ),
            create_button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_ACTION_DISABLE,
            ),
        ),
    )
    
    return components


def build_butcher_option_component(
    user_id, initial_item, butchered_item, seed, butcher_flags, multiplier, index
):
    """
    Builds a butcher option component (section).
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    initial_item : ``Item`
        The item initially butchered.
    
    butchered_item : ``None | Item``
        The just butchered item-
    
    seed : `int`
        Seed to use for butchering.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    index : `int`
        The index of the item.
    
    Returns
    -------
    component : ``Component``
    """
    options_butcher = (initial_item if butchered_item is None else butchered_item).options_butcher
    if (options_butcher is None):
        loot_chance_and_amounts = None
        energy_cost = 0
        custom_id = CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_BUILDER(user_id, initial_item.id, index)
        enabled = False
    else:
        loot_chance_and_amounts = butcher_estimate_loot_chance_and_amounts(options_butcher, multiplier)
        energy_cost = butcher_estimate_energy_cost(options_butcher, multiplier)
        if butchered_item is None:
            custom_id = CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_BUILDER(user_id, initial_item.id)
        else:
            custom_id = CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_BUILDER(
                user_id, initial_item.id, seed, butcher_flags, index, multiplier
            )
        enabled = True
    
    return create_section(
        create_text_display(
            ''.join([*produce_butcher_item_description(
                (initial_item if butchered_item is None else butchered_item), loot_chance_and_amounts, energy_cost)]
            )
        ),
        thumbnail = create_button('Butcher', custom_id = custom_id, enabled = enabled),
    )


def build_butcher_components(
    user,
    guild_id,
    initial_item,
    seed,
    butcher_flags,
    multiplier,
    butcher_amounts_accumulated,
    energy_cost_accumulated,
    butcherables,
    butchered_item,
    butcher_amounts,
    energy_cost,
    now,
    recovering_until,
):
    """
    Builds butcher components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user invoking the interaction.
    
    guild_id : `int`
        The local guild's identifier.
    
    initial_item : ``Item``
        Item to butcher.
    
    seed : `int`
        Seed to use for butchering.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    now : `DateTime`
        The current date time.
    
    recovering_until : `None | DateTime`
        Until when the user is recovering for.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # ---- Header ----
    
    components.append(
        create_section(
            create_text_display(''.join([*produce_butcher_header(initial_item)])),
            thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
        ),
    )
    
    # --- Body ----
    
    if butchered_item is None:
        # If the user did not butcher anything yet, just offer them to butcher the initial item.
        components.append(
            build_butcher_option_component(user.id, initial_item, None, seed, butcher_flags, multiplier, 0)
        )
    
    else:
        # Add what the user just butchered.
        components.append(create_text_display(
            ''.join([*produce_butcher_step_description(butchered_item, butcher_amounts, energy_cost)])
        ))
        
        # Offer the user to further butcher additional parts.
        # Show only the first 10, so we do not pass the component limit.
        if (butcherables is not None):
            for nested_item, index in islice(butcherables, 0, 10):
                components.append(
                    build_butcher_option_component(
                        user.id, initial_item, nested_item, seed, butcher_flags, multiplier, index
                    )
                )
        
        # Summarise how much the user already butchered if it is not the first butcher.
        if (butcher_amounts_accumulated != butcher_amounts) or (energy_cost_accumulated != energy_cost):
            components.append(create_text_display(
                ''.join([*produce_butcher_done_description(butcher_amounts_accumulated, energy_cost_accumulated)])
            ))
    
    # ---- Footer ----
    
    if (recovering_until is not None):
        components.append(create_separator())
        components.append(create_text_display(
            ''.join([*produce_butcher_recovering_until_footer(now, recovering_until)])
        ))
    
    return components
