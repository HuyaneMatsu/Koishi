import vampytest

from ..content_building import produce_error_message_adventure_duration_out_of_threshold


def _iter_options():
    yield (
        True,
        100,
        1000,
        'Duration under lower threshold: 1 minute, 40 seconds < 16 minutes, 40 seconds.',
    )
    
    yield (
        False,
        1000,
        100,
        'Duration over upper threshold: 16 minutes, 40 seconds > 1 minute, 40 seconds.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_error_message_adventure_duration_out_of_threshold(lower, duration, threshold):
    """
    Tests whether ``produce_error_message_adventure_duration_out_of_threshold`` works as intended.
    
    Parameters
    ----------
    lower : `bool`
        Whether it is the lower threshold the duration is out of.
    
    duration : `int`
        Give duration.
    
    threshold : `int`
        Threshold.
    
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_error_message_adventure_duration_out_of_threshold(lower, duration, threshold)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
