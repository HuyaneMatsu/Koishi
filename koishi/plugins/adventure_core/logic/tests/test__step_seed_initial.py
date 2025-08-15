import vampytest

from ..seed_stepping import step_seed_initial


def _iter_options():
    # Do not step if too low.
    yield (
        ((123 << 42) | (555 << 0)),
        0,
        ((123 << 42) | (555 << 0)),
    )
    
    # Do not step if too low.
    yield (
        ((123 << 42) | (555 << 0)),
        1,
        ((123 << 42) | (555 << 0)),
    )
    
    # Step once
    yield (
        ((123 << 42) | (555 << 0)),
        2,
        ((123 << 0) | (555 << 22)),
    )
    
    # Step twice
    yield (
        ((123 << 42) | (555 << 0)),
        3,
        ((123 << 22) | (555 << 44)),
    )
    
    # Overstep (zero)
    yield (
        ((123 << 42) | (555 << 0)),
        33,
        ((123 << 42) | (555 << 0)),
    )
    
    # Overstep (once)
    yield (
        ((123 << 42) | (555 << 0)),
        34,
        ((123 << 0) | (555 << 22)),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__step_seed_initial(seed, action_count):
    """
    tests whether ``step_seed_initial`` works as intended.
    
    Parameters
    ----------
    seed : `int`
        Seed to step.
    
    action_count : `int`
        The amount of actions the adventure has.
    
    Returns
    -------
    output : `int`
    """
    output = step_seed_initial(seed, action_count)
    vampytest.assert_instance(output, int)
    return output
