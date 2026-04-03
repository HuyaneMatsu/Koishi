import vampytest

from hata import Client

from ..headers import get_header_for


def test__get_header_for__hit():
    """
    Tests whether ``get_header_for`` works as intended.
    
    Case: hit.
    """
    client_id = 202312090004
    
    header = 'ayaya'
    
    headers = {
        client_id: (header, header)
    }
    
    client = Client(
        token = 'token_20231209_0004',
        client_id = client_id,
    )
    
    try:
        mocked = vampytest.mock_globals(get_header_for, HEADERS = headers)
        
        output = mocked(client)
        
        vampytest.assert_eq(output, header)
    finally:
        client._delete()
        client = None


def test__get_header_for__miss():
    """
    Tests whether ``get_header_for`` works as intended.
    
    Case: miss.
    """
    client_id = 202312090005
    
    header = 'ayaya'
    
    client = Client(
        token = 'token_20231209_0005',
        client_id = client_id,
    )
    
    try:
        mocked = vampytest.mock_globals(get_header_for, HEADER_DEFAULT = header)
        
        output = mocked(client)
        
        vampytest.assert_eq(output, header)
    finally:
        client._delete()
        client = None
