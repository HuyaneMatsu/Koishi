import vampytest

from ..helpers import _build_non_links_error


def test__build_non_links_error():
    """
    Tests whether ``_build_non_links_error`` works as intended``.
    """
    directory_path = '/root/koishi'
    non_links = ['hey', 'mister']
    
    output = _build_non_links_error(directory_path, non_links)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'Directory: {directory_path!r} contains not only links:\n'
            f'- {non_links[0]!r}\n'
            f'- {non_links[1]!r}'
        ),
    )
