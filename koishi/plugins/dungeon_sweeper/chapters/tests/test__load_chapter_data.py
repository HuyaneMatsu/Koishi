from io import StringIO
from os.path import join as join_paths

import vampytest
from scarletio import to_json

from ..constants import CHAPTERS_PATH
from ..loading_and_saving import load_chapter_data


def test__load_chapter_data():
    """
    Tests whether ``load_chapter_data`` works as intended.
    """
    data = 'aaaa'
    file_name = 'orin.json'
    
    def mock_open(path, mode):
        nonlocal data
        nonlocal file_name
        
        vampytest.assert_eq(path, join_paths(CHAPTERS_PATH, file_name))
        vampytest.assert_eq(mode, 'r')
        
        io = StringIO()
        io.write(to_json(data))
        io.seek(0)
        
        return io
    
    mocked = vampytest.mock_globals(load_chapter_data, open = mock_open)
    
    output = mocked(file_name)
    
    vampytest.assert_instance(output, str)
