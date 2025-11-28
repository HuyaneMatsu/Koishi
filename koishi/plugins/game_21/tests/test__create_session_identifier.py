import vampytest

from ..helpers import create_session_identifier


def test__create_session_identifier():
    """
    Tests whether ``create_session_identifier`` works as intended.
    """
    output = create_session_identifier()
    vampytest.assert_instance(output, int)
