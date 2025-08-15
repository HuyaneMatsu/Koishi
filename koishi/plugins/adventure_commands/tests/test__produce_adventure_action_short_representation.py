from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, AdventureAction

from ..component_builders import produce_adventure_action_short_representation


def _iter_options():
    adventure_entry_id = 9993
    
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        f'<t:{created_at.timestamp():.0f}:T> Gardening'
    )
    
    adventure_entry_id = 9993
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        999999,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        f'<t:{created_at.timestamp():.0f}:T> Unknown'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_action_short_representation(adventure_action):
    """
    Tests whether ``produce_adventure_action_short_representation`` works as intended.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce short representation of.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_action_short_representation(adventure_action)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
