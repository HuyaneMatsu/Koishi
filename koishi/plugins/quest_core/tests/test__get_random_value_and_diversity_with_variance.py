from random import Random

import vampytest

from ..quest_batch_generation import get_random_value_and_diversity_with_variance


def test__get_random_value_and_diversity_with_variance():
    """
    Tests whether ``get_random_value_and_diversity_with_variance`` works as intended.
    """
    random_number_generator = Random()
    base = 100
    require_multiple_of = 10
    variance_percentage_lower_threshold = 85
    variance_percentage_upper_threshold = 115
    
    value, diversity = get_random_value_and_diversity_with_variance(
        random_number_generator,
        base,
        require_multiple_of,
        variance_percentage_lower_threshold,
        variance_percentage_upper_threshold,
    )
    
    vampytest.assert_instance(value, int)
    vampytest.assert_instance(diversity, float)
    vampytest.assert_eq(value > base, diversity > 1.0)
    vampytest.assert_eq(value % require_multiple_of, 0)
    vampytest.assert_true(value >= base * variance_percentage_lower_threshold * 0.01)
    vampytest.assert_true(value <= base * variance_percentage_upper_threshold * 0.01)
