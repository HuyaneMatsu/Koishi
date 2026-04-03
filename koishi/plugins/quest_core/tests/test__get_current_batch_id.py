import vampytest

from ..utils import get_current_batch_id


def test__get_current_batch_id():
    """
    Tests whether ``get_current_batch_id`` works as intended.
    """
    output = get_current_batch_id()
    vampytest.assert_instance(output, int)
