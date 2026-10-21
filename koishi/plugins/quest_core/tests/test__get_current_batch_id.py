import vampytest

from ..utils import get_current_batch_id


def test__get_current_batch_id():
    output = get_current_batch_id()
    vampytest.assert_instance(output, int)
