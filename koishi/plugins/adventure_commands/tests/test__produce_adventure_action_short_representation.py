import vampytest

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, adventure_action_create

from ..content_building import produce_adventure_action_short_representation


def _iter_options():
    created_at = 1463184000
    
    adventure_action = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        f'<t:{created_at}:T> Gardening',
    )
    
    adventure_action = adventure_action_create(
        999999,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure_action,
        f'<t:{created_at}:T> Unknown',
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
