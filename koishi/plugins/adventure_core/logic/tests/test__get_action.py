import vampytest

from ...action import ACTION_TYPE_FORAGING, Action
from ...adventure import Adventure
from ...options import OptionLoot
from ...target import Target


from ..helpers import get_action


def _iter_options():
    target_id_0 = 1333
    target_id_1 = 1336
    action_id_0 = 1334
    action_id_1 = 1335
    
    action_0 = Action(
        action_id_0,
        ACTION_TYPE_FORAGING,
        3600,
        2,
        None,
        (
            OptionLoot(1, 1, 10, 20, 888, 10, 5, 40, 25),
        ),
    )
    
    action_1 = Action(
        action_id_1,
        ACTION_TYPE_FORAGING,
        3600,
        2,
        None,
        (
            OptionLoot(1, 1, 10, 10, 888, 10_000, 10, 40, 25),
        ),
    )
    
    target_0 = Target(
        target_id_0,
        'pudding',
        0,
        (
            action_id_0,
            action_id_1,
        ),
    )
    
    
    adventure_0 = Adventure(
        202507300010,
        9999,
        target_id_0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure_0.action_count = 3
    adventure_0.seed = (123 << 42) | (142 << 0)
    
    
    adventure_1 = Adventure(
        202507300011,
        9999,
        target_id_1,
        0,
        0,
        0,
        0,
        0,
    )
    adventure_1.action_count = 3
    adventure_1.seed = (123 << 42) | (142 << 0)
    
    # generic hit
    yield (
        adventure_0,
        (123 << 22) | (142 << 44),
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
        (123 << 22) | (142 << 44),
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
        (123 << 22) | (142 << 44),
        {
            target_id_0 : target_0,
        },
        {},
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_action(adventure, seed, targets, actions):
    """
    Tests whether ``get_action`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    
    seed : `int`
        Seed used for randomization.
    
    targets : ``dict<int, Target>``
        Mock targets.
    
    actions : ``dict<int, Action>``
        Mock actions.
    
    Returns
    -------
    action_and_seed : ``None | (Action, int)``
    """
    mocked = vampytest.mock_globals(
        get_action,
        TARGETS = targets,
        ACTIONS = actions,
    )
    
    output = mocked(adventure, seed)
    vampytest.assert_instance(output, Action, nullable = True)
    return output
