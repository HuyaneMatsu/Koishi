import vampytest

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, adventure_action_create

from ..content_building import produce_adventure_action_view_description


def _iter_options():
    created_at = 1463184000
    
    adventure_action = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        created_at,
        None,
        None,
        20,
        10,
    )
    
    yield (
        adventure_action,
        (
            f'Occurred at: <t:{created_at}:T>\n'
            f'Used health: 20\n'
            f'Used energy: 10'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_action_view_description(adventure_action):
    """
    Tests whether ``produce_adventure_action_view_description`` works as intended.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce description for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_action_view_description(adventure_action)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
