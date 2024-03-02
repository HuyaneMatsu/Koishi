import vampytest
from hata import Client

from ..utils import _clients_sort_key


def test__clients_sort_key():
    """
    Tests whether ``_clients_sort_key`` works as intended.
    """
    client_id = 202402260000
    client_name = 'koishi'
    
    client = Client(
        'token' + str(client_id),
        client_id = client_id,
        name = client_name,
    )
    
    try:
        output = _clients_sort_key(client)
        
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, client_name)
    
    finally:
        FEATURE_CLIENTS = None
        client._delete()
        client = None
