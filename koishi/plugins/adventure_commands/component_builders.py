__all__ = ()

from datetime import timedelta as TimeDelta

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import (
    DATETIME_FORMAT_CODE, InteractionForm, create_button, create_row, create_section, create_separator,
    create_text_display, elapsed_time, format_datetime
)

from ..adventure_core import (
    ACTIONS, ACTION_TYPE_ARRIVAL, ACTION_TYPE_BUTCHERING, ACTION_TYPE_CANCELLATION, ACTION_TYPE_ENCOUNTER,
    ACTION_TYPE_FATALITY, ACTION_TYPE_FISHING, ACTION_TYPE_FORAGING, ACTION_TYPE_GARDENING, ACTION_TYPE_HUNT,
    ACTION_TYPE_NONE, ACTION_TYPE_TRAP, ACTION_TYPE_UNKNOWN, ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_CANCELLED,
    ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_FINALIZED, ADVENTURE_STATE_RETURNING, LOCATIONS,
    LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY, LOOT_STATE_SUCCESS, TARGETS,
    can_cancel_adventure, get_duration_till_recovery_end, iter_loot_data, produce_auto_cancellation_conditions,
    produce_duration_suggestion
)
from ..item_core import get_item, produce_weight

from .custom_ids import (
    ADVENTURE_ACTION_BATTLE_LOGS_BUILDER, ADVENTURE_ACTION_LISTING_VIEW_BUILDER, ADVENTURE_ACTION_VIEW_BUILDER,
    ADVENTURE_ACTION_VIEW_DEPART, ADVENTURE_ACTION_VIEW_RETURN, ADVENTURE_CANCEL_BUILDER,
    ADVENTURE_CREATE_CONFIRM_BUILDER, ADVENTURE_LISTING_VIEW_BUILDER, ADVENTURE_VIEW_BUILDER
)


ACTION_TYPE_NAME_DEFAULT = 'Unknown'

ACTION_TYPE_TO_NAME = {
    ACTION_TYPE_NONE : 'Nothing',
    ACTION_TYPE_CANCELLATION : 'Cancellation',
    ACTION_TYPE_ARRIVAL : 'Arrival',
    ACTION_TYPE_FATALITY : 'Fatality',
    ACTION_TYPE_UNKNOWN : ACTION_TYPE_NAME_DEFAULT,
    
    ACTION_TYPE_GARDENING : 'Gardening',
    ACTION_TYPE_FORAGING : 'Foraging',
    ACTION_TYPE_BUTCHERING : 'Butchering',
    
    ACTION_TYPE_FISHING : 'Fishing',
    ACTION_TYPE_ENCOUNTER : 'Encounter',
    ACTION_TYPE_HUNT : 'Hunt',
    
    ACTION_TYPE_TRAP : 'Trapped',
}


ACTIVE_ADVENTURE_ACTION_LIMIT = 5
ADVENTURE_ACTION_LISTING_PAGE_SIZE = 10
ADVENTURE_LISTING_PAGE_SIZE = 10


def produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation):
    """
    Produces an adventure's initial representation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
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
    
    Yields
    ------
    part : `str`
    """
    yield 'Location: '
    yield location.name
    
    yield '\nTarget: '
    yield target.name
    
    yield '\nDuration: '
    yield from produce_duration_suggestion(duration)
    
    yield '\nReturn: '
    yield return_.name
    
    yield '\nAuto-cancellation: '
    yield auto_cancellation.name
    yield ' ('
    yield from produce_auto_cancellation_conditions(auto_cancellation)
    yield ')'


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
        ADVENTURE_CREATE_CONFIRM_BUILDER(
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    user_id,
                    adventure_entry_id, 
                    False,
                    0,
                ),
            ),
        ),
    ]


def produce_adventure_cancellation_confirmation_description(adventure):
    """
    Produces an adventure cancellation confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Yields
    ------
    part : `str`
    """
    yield 'Are you sure to cancel your adventure towards '
    yield from _produce_adventure_location_for_headers(adventure)
    yield '?'


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
    return InteractionForm(
        'Confirm adventure cancellation',
        [
            create_text_display(''.join([*produce_adventure_cancellation_confirmation_description(adventure)]))
        ],
        ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
    )


def build_adventure_cancellation_components():
    """
    Builds adventure successful cancellation components.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('You successfully cancelled your adventure.'),
        create_text_display('You head back home immediately.'),
    ]


def _produce_adventure_location_for_headers(adventure):
    """
    Helper function to produce adventure location for headers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce for.
    
    Yields
    ------
    part : `str`
    """
    try:
        location = LOCATIONS[adventure.location_id]
    except KeyError:
        location_name = 'unknown'
    else:
        location_name = location.name
    
    try:
        target = TARGETS[adventure.target_id]
    except KeyError:
        target_name = 'unknown'
    else:
        target_name = target.name
    
    yield location_name
    yield ' for '
    yield target_name


def produce_adventure_view_header(adventure):
    """
    Produces an adventure view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### Adventure to '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_adventure_return_notification_header(adventure):
    """
    Produces an adventure return notification header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### You have returned from adventure at '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_adventure_return_notification_description(adventure):
    """
    Produces an adventure return notification description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Yields
    ------
    part : `str`
    """
    duration = get_duration_till_recovery_end(adventure)
    until = adventure.updated_at + TimeDelta(seconds = duration)
    
    yield 'You are recovering for '
    yield elapsed_time(RelativeDelta(seconds = duration))
    yield ', until '
    yield format_datetime(until, 'T')
    yield '.'


def produce_adventure_action_listing_view_header(adventure, page_index):
    """
    Produces an adventure action listing view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    page_index : `int`
        The shown page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '### Actions of '
    yield from _produce_adventure_location_for_headers(adventure)
    yield ' (page '
    yield str(page_index + 1)
    yield ')'


def produce_adventure_listing_view_header(page_index):
    """
    Produces adventure listing view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    page_index : `int`
        The shown page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '### Adventures (page '
    yield str(page_index + 1)
    yield ')'


def produce_adventure_short_representation(adventure):
    """
    Produces short representation of an adventure for adventure listing view.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce representation for.
    
    Yields
    ------
    part : `str`
    """
    yield format(adventure.created_at, DATETIME_FORMAT_CODE)
    yield ' UTC '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_used(name, initial, exhausted):
    """
    Produces a generic used value without unit.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The name of the used value.
    
    initial : `int`
        Initial value.
    
    exhausted : `int`
        The exhausted amount.
    
    Yields
    ------
    part : `str`
    """
    yield 'Used '
    yield name
    yield ': '
    yield str(exhausted)
    yield ' / '
    yield str(initial)


def produce_adventure_view_description_active(adventure, now, inventory_total, inventory_exhausted):
    """
    Produces adventure description for an active adventure.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    now : `DateTime`
        The current time.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Yields
    ------
    part : `str`
    """
    yield 'Departed at: '
    yield format(adventure.created_at, DATETIME_FORMAT_CODE)
    yield ' UTC\n'
    yield from produce_used('health', adventure.health_initial, adventure.health_exhausted)
    yield '\n'
    yield from produce_used('energy', adventure.energy_initial, adventure.energy_exhausted)
    yield '\nUsed inventory: '
    yield from produce_weight(inventory_exhausted)
    yield ' / '
    yield from produce_weight(inventory_total)
    yield ' kg\nElapsed time: '
    yield elapsed_time(RelativeDelta(adventure.created_at, now))
    
    adventure_state = adventure.state
    if adventure_state == ADVENTURE_STATE_DEPARTING:
        next_step_description = 'departing to the location'
    
    elif adventure_state == ADVENTURE_STATE_ACTIONING:
        next_step_description = 'working on your target task'
    
    elif adventure_state == ADVENTURE_STATE_CANCELLED or adventure_state == ADVENTURE_STATE_RETURNING:
        next_step_description = 'returning home'
    
    elif adventure_state == ADVENTURE_STATE_FINALIZED:
        next_step_description = None
    
    else:
        next_step_description = None
    
    if (next_step_description is not None):
        yield '\nYou are currently '
        yield next_step_description
        yield '.'


def produce_adventure_view_description_finalized(adventure):
    """
    Produces adventure description for an active adventure.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Yields
    ------
    part : `str`
    """
    yield 'Departed at: '
    yield format(adventure.created_at, DATETIME_FORMAT_CODE)
    yield ' UTC\n'
    yield from produce_used('health', adventure.health_initial, adventure.health_exhausted)
    yield '\n'
    yield from produce_used('energy', adventure.energy_initial, adventure.energy_exhausted)
    yield '\nTotal duration: '
    yield elapsed_time(RelativeDelta(adventure.created_at, adventure.updated_at))
    yield '\nRecovery time: '
    yield elapsed_time(RelativeDelta(seconds = get_duration_till_recovery_end(adventure)))


def _produce_adventure_action_type_for_headers(adventure_action):
    """
    Helper function to produce adventure action type for headers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce for.
    
    Yields
    ------
    part : `str`
    """
    try:
        action = ACTIONS[adventure_action.action_id]
    except KeyError:
        action_name = ACTION_TYPE_NAME_DEFAULT
    else:
        action_name = ACTION_TYPE_TO_NAME.get(action.type, ACTION_TYPE_NAME_DEFAULT)
    
    yield action_name


def produce_adventure_action_short_representation(adventure_action):
    """
    Produces an adventure action's header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield format_datetime(adventure_action.created_at, 'T')
    yield ' '
    yield from _produce_adventure_action_type_for_headers(adventure_action)


def produce_adventure_action_view_header(adventure_action):
    """
    Produces an adventure action's header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### Action '
    yield from _produce_adventure_action_type_for_headers(adventure_action)


def produce_adventure_action_view_description(adventure_action):
    """
    Produces an adventure action's description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce description for.
    
    Yields
    ------
    part : `str`
    """
    yield 'Occurred at: '
    yield format_datetime(adventure_action.created_at, 'T')
    yield '\nUsed health: '
    yield str(adventure_action.health_exhausted)
    yield '\nUsed energy: '
    yield str(adventure_action.energy_exhausted)


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


def _item_and_amount_pair_sort_key_getter(item):
    """
    Sort key getter for item and amount pair items.
    
    Parameters
    ----------
    item : ``(Item, int)``
        Item to get sort key for.
    
    Returns
    -------
    key : `str`
    """
    return item[0].name


def produce_loot_listing(grouped_loot):
    """
    Produces loot listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    grouped_loot : `dict<int, dict<int, int>>`
        Grouped loot by state.
    
    Yields
    ------
    part : `str`
    """
    group_added = False
    
    for loot_state, title in (
        (LOOT_STATE_SUCCESS, 'Loot'),
        (LOOT_STATE_LOST_DUE_LOW_ENERGY, 'Loot lost due to low energy'),
        (LOOT_STATE_LOST_DUE_FULL_INVENTORY, 'Loot lost due to full inventory'),
    ):
        try:
            group = grouped_loot[loot_state]
        except KeyError:
            continue
        
        if group_added:
            yield '\n'
        else:
            group_added = True
        
        yield '### '
        yield title
        yield ':'
        
        for item, amount in sorted(
            ((get_item(item_id), amount) for (item_id, amount) in group.items()),
            key = _item_and_amount_pair_sort_key_getter,
        ):
            yield '\n- '
            
            emoji = item.emoji
            if (emoji is not None):
                yield emoji.as_emoji
                yield ' '
            
            yield item.name
            yield ' x'
            yield str(amount)


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
                custom_id = ADVENTURE_ACTION_VIEW_DEPART,
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
                    custom_id = ADVENTURE_ACTION_VIEW_BUILDER(
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
                custom_id = ADVENTURE_ACTION_VIEW_RETURN,
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to adventures',
                enabled = allow_switching_to_adventure_listing_view,
                custom_id = ADVENTURE_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'View all action',
                enabled = (True if truncated_count else False),
                custom_id = ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                    0,
                ),
            ),
            create_button(
                'Cancel',
                enabled = can_cancel_adventure(adventure),
                custom_id = ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id, 
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to adventures',
                enabled = allow_switching_to_adventure_listing_view,
                custom_id = ADVENTURE_LISTING_VIEW_BUILDER(
                    adventure.user_id,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'View all action',
                custom_id = ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
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
                custom_id = ADVENTURE_CANCEL_BUILDER(adventure.user_id, adventure.entry_id),
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    user_id,
                    adventure_action.adventure_entry_id,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                'Back to actions',
                enabled = allow_switching_to_adventure_action_listing_view,
                custom_id = ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
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
                custom_id = ADVENTURE_ACTION_BATTLE_LOGS_BUILDER(
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    allow_switching_to_adventure_listing_view,
                    adventure_listing_page_index,
                ),
            ),
            create_button(
                f'Page {adventure_action_listing_page_index}',
                custom_id = ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
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
                custom_id = ADVENTURE_ACTION_LISTING_VIEW_BUILDER(
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
                        custom_id = ADVENTURE_VIEW_BUILDER(
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
                custom_id = ADVENTURE_LISTING_VIEW_BUILDER(
                    user_id, max(0, adventure_listing_page_index - 1),
                ),
                enabled = (adventure_listing_page_index > 0),
            ),
            create_button(
                f'Page {adventure_listing_page_index + 2}',
                custom_id = ADVENTURE_LISTING_VIEW_BUILDER(
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
                custom_id = ADVENTURE_VIEW_BUILDER(
                    adventure.user_id,
                    adventure.entry_id,
                    False,
                    0,
                ),
            ),
        ),
    )
    
    return components


def produce_adventure_depart_failure_recovery_description(recovering_until, now):
    """
    Produces adventure depart failure message for the case when the user is recovering.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    recovering_until : `DateTine`
        Until when the user is recovering.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    yield 'You are currently recovering for '
    yield elapsed_time(RelativeDelta(recovering_until, now))
    yield ', until '
    yield format_datetime(recovering_until, 'T')
    yield '.\nYou cannot go on an adventure in the meantime.'
