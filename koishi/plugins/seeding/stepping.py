__all__ = ('step_seed', 'step_seed_initial')


ADVENTURE_SEED_STEP_SHIFT = 22
ADVENTURE_SEED_STEP_MASK_SHIFT = 64 - ADVENTURE_SEED_STEP_SHIFT
ADVENTURE_SEED_STEP_MASK = ((1 << (ADVENTURE_SEED_STEP_SHIFT + 1)) - 1) << ADVENTURE_SEED_STEP_MASK_SHIFT


def step_seed_initial(seed, action_count):
    """
    Steps the seed `action_count` times.
    
    Parameters
    ----------
    seed : `int`
        Seed to step.
    
    action_count : `int`
        The amount of actions the adventure has.
    
    Returns
    -------
    seed : `int`
    """
    if action_count <= 0:
        return seed
    
    # After the 31th stepping we repeat, so reduce the amount of steps.
    action_count &= 31
    
    for _ in range(action_count):
        seed = step_seed(seed)
    
    return seed


def step_seed(seed):
    """
    Steps the seed.
    
    Parameters
    ----------
    seed : `int`
        Seed to step.
    
    Returns
    -------
    seed : `int`
    """
    # Here we separate the seed to 2 parts:
    # - Upper "n" bits
    # - Lower "m" bits
    # We move the lower "m" bits up to create enough space for the upper "n" bits.
    # We move the upper "n" bits to start at 0.
    # We merge the 2 newly created parts together.
    return (
        ((seed & ADVENTURE_SEED_STEP_MASK) >> ADVENTURE_SEED_STEP_MASK_SHIFT) |
        ((seed &~ ADVENTURE_SEED_STEP_MASK) << ADVENTURE_SEED_STEP_SHIFT)
    )
