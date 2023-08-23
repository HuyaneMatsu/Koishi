from collections import deque
from hata import CLIENTS, USERS, KOKORO
from scarletio import Task


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
USER_CACHE = deque(maxlen = USER_CACHE_SIZE)

def _get_client():
    return next(_CLIENT_ITERATOR)


async def get_user(user_id):
    try:
        user = USERS[user_id]
    except KeyError:
        pass
    else:
        return user
    
    return await _get_user_async(user_id)


async def _get_user_async(user_id):
    client = _get_client()
    user = await client.user_get(user_id)
    USER_CACHE.append(user)
    return user


async def get_users_unordered(user_ids):
    tasks = None
    users = []
    
    for user_id in user_ids:
        try:
            user = USERS[user_id]
        
        except KeyError:
            if tasks is None:
                tasks = []
            
            task = Task(KOKORO, _get_user_async(user_id))
            tasks.append(task)
        
        else:
            users.append(user)
    
    if (tasks is not None):
        for task in tasks:
            try:
                user = await task
            except:
                for task in tasks:
                    task.cancel()
                
                raise
            
            users.append(user)
    
    return users
