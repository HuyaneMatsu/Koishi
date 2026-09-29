__all__ = (
    'adventure_action_group_loot_by_state', 'adventure_action_listing_accumulate_loot',
    'adventure_action_listing_group_loot_by_state'
)

from scarletio import export

from .loot_packing_and_unpacking import loot_data_iter


def _adventure_action_accumulate_group_loot_by_state(adventure_action, grouped_loot):
    """
    Helper function to accumulate group a single adventure action's loot.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to group its loot of.
    
    grouped_loot : `dict<int, dict<int, int>>`
        Already accumulated loot.
    """
    for loot_state, item_id, amount in loot_data_iter(adventure_action.loot_data):
        try:
            group = grouped_loot[loot_state]
        except KeyError:
            group = {}
            grouped_loot[loot_state] = group
        else:
            amount += group.get(item_id, 0)
        
        group[item_id] = amount


def adventure_action_listing_group_loot_by_state(adventure_action_listing):
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
            _adventure_action_accumulate_group_loot_by_state(adventure_action, grouped_loot)
    
    return grouped_loot


def adventure_action_group_loot_by_state(adventure_action):
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
    _adventure_action_accumulate_group_loot_by_state(adventure_action, grouped_loot)
    return grouped_loot


def _adventure_action_accumulate_loot(adventure_action, accumulated_loot):
    """
    Helper function to accumulate an adventure action's loot.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to accumulate its loot of.
    
    accumulated_loot : `dict<int, int>`
        Already accumulated loot.
    """
    for loot_state, item_id, amount in loot_data_iter(adventure_action.loot_data):
        accumulated_loot[item_id] = accumulated_loot.get(item_id, 0) + amount


@export
def adventure_action_listing_accumulate_loot(adventure_action_listing):
    """
    Accumulates looted items.
    
    Parameters
    ----------
    adventure_action_listing : ``None | list<AdventureAction>``
        Adventure action listing to accumulate loot of.
    
    Returns
    -------
    accumulated_loot : `dict<int, int>`
    """
    accumulated_loot = {}
    
    if (adventure_action_listing is not None):
        for adventure_action in adventure_action_listing:
            _adventure_action_accumulate_loot(adventure_action, accumulated_loot)
    
    return accumulated_loot
