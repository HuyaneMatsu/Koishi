import vampytest

from ..interactions import get_censor_reason_for_message_content


def _iter_options():
    yield 'hey mister', type(None)
    yield 'ayaya https://orindance.party/ ayaya', str
    yield 'ayaya discord.gg/koishi ayaya', str
    

@vampytest.call_from(_iter_options())
def test__get_censor_reason_for_message_content(input_value, expected_output_type):
    """
    Tests whether ``get_censor_reason_for_message_content`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test.
    expected_output_type : `type`
        Type to expect the output to be.
    """
    output = get_censor_reason_for_message_content(input_value)
    vampytest.assert_instance(output, expected_output_type)
