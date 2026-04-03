__all__ = ()

from math import floor


def round_value(value, require_multiple_of):
    """
    Rounds the given value to the closest multiple.
    
    Parameters
    ----------
    value : `int`
        Value to round.
    
    require_multiple_of : `int`
        Value to require the output to be multiple of.
    
    Returns
    -------
    value : `int`
    """
    if require_multiple_of != 1:
        fraction = value % require_multiple_of
        value -= fraction
        if fraction > require_multiple_of >> 1:
            value += require_multiple_of
    return value


def get_random_value_and_diversity_with_variance(
    random_number_generator,
    base,
    require_multiple_of,
    variance_percentage_lower_threshold,
    variance_percentage_upper_threshold,
):
    """
    Returns a random value for the given variance.
    
    Parameters
    ----------
    random_number_generator : `random.Random`
        Random number generator.
    
    base : `int`
        Base value.
    
    variance_percentage_lower_threshold : `int`
        Lower variance percentage threshold.
    
    variance_percentage_upper_threshold : `int`
        Upper variance percentage threshold.
    
    Returns
    -------
    value_with_diversity : `(int, float)`
    """
    variance_percentage = (
        variance_percentage_lower_threshold +
        floor(
            random_number_generator.random() *
            (variance_percentage_upper_threshold - variance_percentage_lower_threshold + 1)
        )
    )
    
    value = floor(base * variance_percentage / 100)
    value = round_value(value, require_multiple_of)
    value = max(value, require_multiple_of)
    diversion = value / base
    return value, diversion
