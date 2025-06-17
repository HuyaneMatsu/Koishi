import vampytest

from ..user_state import get_first_stage_id


def test__get_first_stage_id():
    """
    Tests whether ``get_first_stage_id`` works as intended.
    """
    output = get_first_stage_id()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
