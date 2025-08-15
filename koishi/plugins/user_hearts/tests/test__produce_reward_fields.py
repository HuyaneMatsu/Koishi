import vampytest

from ..rendering import produce_reward_fields


def _iter_options():
    yield (
        None,
        0,
        0,
        0,
        (
            ''
        ),
    )
    
    yield (
        None,
        2,
        0,
        0,
        (
            'Base: 2\n'
        ),
    )
    
    yield (
        None,
        0,
        2,
        0,
        (
            'Extra limit: 2\n'
        ),
    )
    
    yield (
        None,
        0,
        0,
        2,
        (
            'Extra per streak: 2\n'
        ),
    )
    
    yield (
        None,
        1,
        2,
        3,
        (
            'Base: 1\n'
            'Extra limit: 2\n'
            'Extra per streak: 3\n'
        ),
    )
    
    yield (
        '+',
        0,
        0,
        0,
        (
            ''
        ),
    )
    
    yield (
        '+',
        1,
        2,
        3,
        (
            '+ Base: 1\n'
            '+ Extra limit: 2\n'
            '+ Extra per streak: 3\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_reward_fields(prefix, base, extra_limit, extra_per_streak):
    """
    Tests whether ``produce_reward_fields`` works as intended.
    
    Parameters
    ----------
    prefix : `None | str`
        Prefix to use if any.
    
    base : `int`
        Reward base.
    
    extra_limit : `int`
        Reward extra limit.
    
    extra_per_streak : `int`
        Reward extra per streak.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_reward_fields(prefix, base, extra_limit, extra_per_streak))
