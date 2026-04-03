__all__ = ('random_index',)

from random import random


def random_index(weights):
    """
    Generates a random index for the given weights.
    
    Parameters
    ----------
    weights : `iterable<int>`
        Weights to generate random index for.
    
    Returns
    -------
    index : `int`
        Returns `-1` on failure.
    """
    if not weights:
        return -1
    
    total_weight = sum(weights)
    if total_weight <= 0.0:
        return 0
    
    value = random() * total_weight
    
    cumulative = 0.0
    for index, weight in enumerate(weights):
        cumulative += weight
        if cumulative >= value:
            return index
    
    return index
