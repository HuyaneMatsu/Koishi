import vampytest

from ..seed_stepping import step_seed


def _iter_options():
    yield (
        ((123 << 42) | (555 << 0)),
        ((123 << 0) | (555 << 22)),
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__step_seed(seed):
    """
    tests whether ``step_seed`` works as intended.
    
    Parameters
    ----------
    seed : `int`
        Seed to step.
    
    Returns
    -------
    output : `int`
    """
    output = step_seed(seed)
    vampytest.assert_instance(output, int)
    return output
