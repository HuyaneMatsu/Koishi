from collections import deque
from hata import CLIENTS, USERS

# Base cache implementation for repeated user requests

def _client_repeater():
    while True:
        if not CLIENTS:
            raise RuntimeError()
        
        try:
            yield from CLIENTS.values()
        except RuntimeError:
            continue

_CLIENT_ITERATOR = iter(_client_repeater())

USER_CACHE_SIZE = 1000
USER_CACHE = deque(maxlen=USER_CACHE_SIZE)

def get_client():
    return next(_CLIENT_ITERATOR)


async def get_user(user_id):
    try:
        user = USERS[user_id]
    except KeyError:
        pass
    else:
        return user
    
    client = get_client()
    user = await client.user_get(user_id)
    USER_CACHE.append(user)
    return user
