from io import BytesIO

import vampytest

from ..data_base_connected import _open_and_write_initial_data_sync


def test___open_and_write_initial_data_sync():
    """
    Tests whether ``_open_and_write_initial_data_sync`` works as intended.
    """
    file_path = '/tmp/test.kd'
    position = 20
    initial_data = b'nyan'
    open_called = False
    open_output = None
    
    def open_patched(input_file_path, mode):
        nonlocal file_path
        nonlocal open_called
        nonlocal open_output
        vampytest.assert_eq(input_file_path, file_path)
        vampytest.assert_eq(mode, 'wb+')
        open_called = True
        open_output = BytesIO()
        return open_output
    
    mocked = vampytest.mock_globals(
        _open_and_write_initial_data_sync,
        open = open_patched,
    )
    
    output = mocked(file_path, position, initial_data)
    vampytest.assert_true(open_called)
    vampytest.assert_is(output, open_output)
    
    written = output.tell() - position
    output.seek(position)
    vampytest.assert_eq(
        output.read(written),
        initial_data,
    )
