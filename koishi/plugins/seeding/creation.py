__all__ = ('create_seed',)

from random import random
from math import floor


def create_seed():
    """
    Creates a seed for adventures and alike.
    
    Returns
    -------
    seed : `int`
    """
    return floor(random() * (1 << 63))
