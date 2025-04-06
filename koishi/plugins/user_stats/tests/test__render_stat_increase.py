import vampytest

from ..embed_builders import _render_stat_increase


def _iter_options():
    yield 10, 10, '10'
    yield 10, 12, '12 (10 + 2)'
    yield 10, 8, '8 (10 - 2)'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_stat_increase(stat_base, stat_calculated):
    """
    Tests whether ``_render_stat_increase`` works as intended.
    
    Parameters
    ----------
    stat_base : `int`
        The base of the stat.
    
    stat_calculated : `int`
        The calculated stats.
    
    Returns
    -------
    output `str`
    """
    output = _render_stat_increase(stat_base, stat_calculated)
    vampytest.assert_instance(output, str)
    return output
