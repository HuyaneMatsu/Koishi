import vampytest

from hata.ext.slash import InteractionResponse

from ..error_message_getter import okuu_error_message_getter


def test__okuu_error_message_getter():
    """
    Tests whether ``okuu_error_message_getter`` works as intended.
    """
    output = okuu_error_message_getter()
    vampytest.assert_instance(output, InteractionResponse)
    vampytest.assert_is(output.content, None)
    vampytest.assert_is_not(output.embed, None)
