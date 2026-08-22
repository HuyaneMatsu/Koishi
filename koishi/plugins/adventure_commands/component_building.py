__all__ = ()

from itertools import islice

from hata import (
    InteractionForm, StringSelectOption, create_button, create_label, create_row, create_section, create_separator,
    create_string_select, create_text_display, create_thumbnail_media, format_datetime
)

from ..adventure_core import (
    ADVENTURE_STATE_FINALIZED, can_cancel_adventure_after, can_cancel_adventure_now, iter_loot_data
)
from ..item_core import butcher_estimate_energy_cost, butcher_estimate_loot_chance_and_amounts
from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_ACTION_DISABLE

from .constants import (
    ACTIVE_ADVENTURE_ACTION_LIMIT, ADVENTURE_ACTION_LISTING_PAGE_SIZE, ADVENTURE_CANCELLATION_MODE_AFTER,
    ADVENTURE_CANCELLATION_MODE_NOW,
)
from .content_building import (
    produce_adventure_action_listing_view_header, produce_adventure_action_notification_header,
    produce_adventure_action_short_representation, produce_adventure_action_view_description,
    produce_adventure_action_view_header, produce_adventure_cancellation_confirmation_description,
    produce_adventure_initial_representation, produce_adventure_listing_view_header,
    produce_adventure_return_notification_description, produce_adventure_return_notification_header,
    produce_adventure_short_representation, produce_adventure_view_description_active,
    produce_adventure_view_description_finalized, produce_adventure_view_header, produce_butcher_done_description,
    produce_butcher_header, produce_butcher_item_description, produce_butcher_recovering_until_footer,
    produce_butcher_step_description, produce_loot_listing
)
from .custom_ids import (
    CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER, CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_BUILDER, CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN, CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_BUILDER,
    CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_BUILDER, CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_BUILDER,
    CUSTOM_ID_ADVENTURE_CANCEL_BUILDER, CUSTOM_ID_ADVENTURE_CANCELLATION_MODE,
    CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_BUILDER, CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER,
    CUSTOM_ID_ADVENTURE_VIEW_BUILDER
)


def build_adventure_create_confirmation_form(
    user_id, location, target, duration, return_, auto_cancellation, enable_interactive_components,
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
    
    enable_interactive_components : `bool`
        Whether interaction components should be enabled.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    return InteractionForm(
        'Confirm your adventure',
        [
            create_text_display(''.join([*
                produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation),
            ])),
        ],
        CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_BUILDER(
            user_id, location.id, target.id, duration, return_.id, auto_cancellation.id
        ),
    )


def build_adventure_create_confirm_components(
    user_id, adventure_entry_id, location, target, duration, return_, auto_cancellation
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
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('### You began your adventure, best of luck brave adventurer!'),
        create_separator(),
        create_text_display(''.join([*
            produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation),
        ])),
        create_separator(),
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    user_id,
                    adventure_entry_id, 
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


def _accumulate_group_adventure_action_loot(adventure_action, grouped_loot):
    """
    Helper function to accumulate group a single adventure action's loot.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to group its loot of.
    
    grouped_loot : `dict<int, dict<int, int>>`
        Already accumulated loot.
    """
    for loot_state, item_id, amount in iter_loot_data(adventure_action.loot_data):
        try:
            group = grouped_loot[loot_state]
        except KeyError:
            group = {}
            grouped_loot[loot_state] = group
        else:
            amount += group.get(item_id, 0)
        
        group[item_id] = amount


def group_adventure_action_listing_loot_by_state(adventure_action_listing):
    """
    Groups looted items by state.
    
    Parameters
    ----------
    adventure_action_listing : ``None | list<AdventureAction>``
        Adventure action listing to group its loot of.
    
    Returns
    -------
    grouped_loot : `dict<int, dict<int, int>>`
    """
    grouped_loot = {}
    
    if (adventure_action_listing is not None):
        for adventure_action in adventure_action_listing:
            _accumulate_group_adventure_action_loot(adventure_action, grouped_loot)
    
    return grouped_loot


def group_adventure_action_loot_by_state(adventure_action):
    """
    Groups looted items by state.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to group its loot of.
    
    Returns
    -------
    grouped_loot : `dict<int, dict<int, int>>`
    """
    grouped_loot = {}
    _accumulate_group_adventure_action_loot(adventure_action, grouped_loot)
    return grouped_loot



def iter_build_adventure_action_components(
    adventure,
    adventure_action_listing,
    produce_depart,
    produce_return,
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
    
    adventure_action_listing : ``None | list<AdventureActions>``
        Adventure actions to render components for.
    
    produce_depart : `bool`
        Whether to produce depart component.
    
    produce_return : `bool`
        Whether to produce return component.
    
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
                f'{format_datetime(adventure.created_at, "T")} Depart'
            ),
            thumbnail = create_button(
                'View',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART,
                enabled = False,
            ),
        )
    
    if (adventure_action_listing is not None):
        for adventure_action in adventure_action_listing:
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
                        adventure_action.entry_id,
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
                f'{format_datetime(adventure.updated_at, "T")} Return'
            ),
            thumbnail = create_button(
                'View',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN,
                enabled = False,
            ),
        )


def build_adventure_view_active_components(
    adventure,
    adventure_action_listing,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    now,
    inventory_total,
    inventory_exhausted,
):
    """
    Builds components for an active adventure describing it.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_action_listing : ``None | list<AdventureActions>``
        The adventure's actions.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    now : `DateTime`
        The current time.
    
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
    
    components.append(
        create_text_display(''.join([*produce_adventure_view_description_active(
            adventure, now, inventory_total, inventory_exhausted
        )])),
    )
    
    components.append(create_separator())
    
    # ---- Loot ----
    
    if (
        (adventure_action_listing is not None) and
        any((adventure_action.loot_data is not None) for adventure_action in adventure_action_listing)
    ):
        components.append(
            create_text_display(''.join([*produce_loot_listing(
                group_adventure_action_listing_loot_by_state(adventure_action_listing)
            )])),
        )
        components.append(create_separator())
    
    # ---- Adventure actions ----
    
    action_count = adventure.action_count + 1
    if (adventure_action_listing is None):
        truncated_count = 0
        produce_depart = True
        adventure_action_listing_to_show = None
    elif action_count <= ACTIVE_ADVENTURE_ACTION_LIMIT:
        truncated_count = 0
        produce_depart = True
        adventure_action_listing_to_show = adventure_action_listing.copy()
    else:
        truncated_count = action_count - ACTIVE_ADVENTURE_ACTION_LIMIT
        produce_depart = False
        adventure_action_listing_to_show = adventure_action_listing[-ACTIVE_ADVENTURE_ACTION_LIMIT:]
    
    if truncated_count:
        components.append(
            create_text_display(
                f'+ {truncated_count} truncated (showing latest {ACTIVE_ADVENTURE_ACTION_LIMIT})'
            )
        )
    
    components.extend(
        iter_build_adventure_action_components(
            adventure,
            adventure_action_listing_to_show,
            produce_depart,
            False, 
            allow_switching_to_adventure_listing_view,
            adventure_listing_page_index,
            False,
            0,
        )
    )
    components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(
        create_row(
            create_button(
                'Refresh',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to adventures',
                enabled = allow_switching_to_adventure_listing_view,
                custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'View all action',
                enabled = (True if truncated_count else False),
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    0,
                ),
            ),
            create_button(
                'Cancel',
                enabled = (can_cancel_adventure_now(adventure) or can_cancel_adventure_after(adventure)),
                custom_id = CUSTOM_ID_ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
            ),
        )
    )
    
    return components


def build_adventure_view_finalized_components(
    adventure,
    adventure_action_listing,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
):
    """
    Builds components for a finalized adventure describing it.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_action_listing : ``None | list<AdventureActions>``
        The adventure's actions.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
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
    
    components.append(
        create_text_display(''.join([*produce_adventure_view_description_finalized(adventure)])),
    )
    
    components.append(create_separator())
    
    # ---- Loot ----
    
    if (
        (adventure_action_listing is not None) and
        any((adventure_action.loot_data is not None) for adventure_action in adventure_action_listing)
    ):
        components.append(
            create_text_display(''.join([*produce_loot_listing(
                group_adventure_action_listing_loot_by_state(adventure_action_listing)
            )])),
        )
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(
        create_row(
            create_button(
                'Refresh',
                enabled = False,
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to adventures',
                enabled = allow_switching_to_adventure_listing_view,
                custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'View all action',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    0,
                ),
            ),
            create_button(
                'Cancel',
                enabled = False,
                custom_id = CUSTOM_ID_ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
            ),
        )
    )
    
    return components


def build_adventure_action_view_components(
    user_id,
    adventure_action,
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
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
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
                group_adventure_action_loot_by_state(adventure_action)
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
                    adventure_action.adventure_entry_id,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to actions',
                enabled = allow_switching_to_adventure_action_listing_view,
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    user_id,
                    adventure_action.adventure_entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    adventure_action_listing_page_index,
                ),
            ),
            create_button(
                'View battle logs',
                enabled = False, # Battles are not implemented yet.
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER(
                    user_id, adventure_action.adventure_entry_id, adventure_action.entry_id
                ),
            ),
        )
    )
    
    return components


def build_adventure_action_listing_view_components(
    adventure,
    adventure_action_listing,
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
    
    adventure_action_listing : ``None | list<AdventureActions>``
        The adventure's actions.
    
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
    adventure_finalized = (adventure.state == ADVENTURE_STATE_FINALIZED)
    action_count = adventure.action_count + 1 + adventure_finalized
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
        produce_return = adventure_finalized and (page_count - adventure_action_listing_page_index == 1)
        
        if adventure_action_listing is None:
            adventure_action_listing_to_show = None
        else:
            adventure_action_listing_to_show = adventure_action_listing[
                max(0, adventure_action_listing_page_index * ADVENTURE_ACTION_LISTING_PAGE_SIZE - 1) :
                (adventure_action_listing_page_index + 1) * ADVENTURE_ACTION_LISTING_PAGE_SIZE - 1
            ]
        
        components.extend(
            iter_build_adventure_action_components(
                adventure,
                adventure_action_listing_to_show,
                produce_depart,
                produce_return,
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
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                f'Page {adventure_action_listing_page_index}',
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
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
    
    # ---- description ----
    
    if adventure.health_exhausted or adventure.energy_exhausted:
        components.append(
            create_separator(),
        )
        components.append(
            create_text_display(''.join([*produce_adventure_return_notification_description(adventure)])),
        )
    
    # ---- Control ----
    
    components.append(
        create_separator(),
    )
    components.append(
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    False,
                    0,
                ),
            ),
        ),
    )
    
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
                group_adventure_action_loot_by_state(adventure_action)
            )])),
        )
        components.append(create_separator())
    
    # ---- Controls ----
    
    components.append(
        create_row(
            create_button(
                'View adventure',
                custom_id = CUSTOM_ID_ADVENTURE_VIEW_BUILDER(
                    adventure.user_id, adventure_action.adventure_entry_id, False, 0,
                ),
            ),
            create_button(
                'View battle logs',
                enabled = False, # Battles are not implemented yet.
                custom_id = CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER(
                    adventure.user_id, adventure_action.adventure_entry_id, adventure_action.entry_id
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
