from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, AdventureAction

from ..component_builders import produce_adventure_action_view_header


def _iter_options():
    adventure_entry_id = 9993
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        '### Action Gardening'
    )
    
    adventure_entry_id = 9993
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        999999,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        '### Action Unknown'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_action_view_header(adventure_action):
    """
    Tests whether ``produce_adventure_action_view_header`` works as intended.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce header for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_action_view_header(adventure_action)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
