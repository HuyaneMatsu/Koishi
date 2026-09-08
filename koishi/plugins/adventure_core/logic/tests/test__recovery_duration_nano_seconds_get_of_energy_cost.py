import vampytest

from ..helpers import recovery_duration_seconds_get_of_energy_cost


def _iter_options():
    yield 1, 120
    yield 100, 12000


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__recovery_duration_seconds_get_of_energy_cost(energy_exhausted):
    """
    Tests whether ``recovery_duration_seconds_get_of_energy_cost`` works as intended.

    Parameters
    ----------
    energy_exhausted : `int`
        The amount of used energy.
    
    Returns
    -------
    output : `int`
    """
    output = recovery_duration_seconds_get_of_energy_cost(energy_exhausted)
    vampytest.assert_instance(output, int)
    return output
