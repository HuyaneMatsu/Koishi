from random import Random

import vampytest

from ...action import ACTION_TYPE_FORAGING, Action, action_create
from ...adventure import adventure_action_create, adventure_create
from ...options import option_loot_create
from ...target import target_create


from ..helpers import action_get


def _iter_options():
    target_id_0 = 1333
    target_id_1 = 1336
    action_id_0 = 1334
    action_id_1 = 1335
    
    action_0 = action_create(
        action_id_0,
        ACTION_TYPE_FORAGING,
        3600,
        2,
        None,
        (
            option_loot_create(False, 1, 1, False, 10, 20, 888, 10, 5, 40, 25),
        ),
    )
    
    action_1 = action_create(
        action_id_1,
        ACTION_TYPE_FORAGING,
        3600,
        2,
        None,
        (
            option_loot_create(False, 1, 1, False, 10, 10, 888, 10_000, 10, 40, 25),
        ),
    )
    
    target_0 = target_create(
        target_id_0,
        'pudding',
        0,
        (
            action_id_0,
            action_id_1,
        ),
    )
    
    
    adventure_0 = adventure_create(
        202507300010,
        9999,
        target_id_0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure_0.action_listing = [
        adventure_action_create(
            100,
            0,
            None,
            None,
            0,
            0,
        ) for _ in range(3)
    ]
    
    # generic hit
    yield (
        adventure_0,
        Random(12),
        {
            target_id_0 : target_0,
        },
        {
            action_id_0 : action_0,
            action_id_1 : action_1,
        },
        action_0,
    )
    
    # miss target
    yield (
        adventure_0,
        Random(12),
        {},
        {
            action_id_0 : action_0,
            action_id_1 : action_1,
        },
        None,
    )
    
    # miss adventure.
    yield (
        adventure_0,
        Random(12),
        {
            target_id_0 : target_0,
        },
        {},
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__action_get(adventure, random, targets, actions):
    """
    Tests whether ``action_get`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    
    random : `random.Random`
        Random number generator to use.
    
    targets : ``dict<int, Target>``
        Mock targets.
    
    actions : ``dict<int, Action>``
        Mock actions.
    
    Returns
    -------
    action : ``None | Action``
    """
    mocked = vampytest.mock_globals(
        action_get,
        TARGETS = targets,
        ACTIONS = actions,
    )
    
    output = mocked(adventure, random)
    vampytest.assert_instance(output, Action, nullable = True)
    return output
