from io import BytesIO
import vampytest

from ..data_base_connected import _write_write_queue_sync


def test__write_write_queue_sync():
    """
    Tests whether ``_write_write_queue_sync`` works as intended.
    """
    write_queue = [(0, b'\001' * 16), (20, b'nyan')]
    sync_io = BytesIO()
    sync_io.write(b'\000' * 20)
    
    _write_write_queue_sync(sync_io, write_queue)
    
    sync_io.seek(0)
    output = sync_io.read(24)
    
    vampytest.assert_eq(
        output,
        b''.join([
            b'\001' * 16,
            b'\000' * 4,
            b'nyan',
        ]),
    )
