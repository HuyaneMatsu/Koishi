__all__ = ()

from hata import KOKORO
from hata.ext.slash import abort
from scarletio import sleep, to_json
from scarletio.web_common.headers import CONTENT_TYPE

from .constants import HEADER_RETRY_AFTER, RATE_LIMIT_LOCK, RATE_LIMIT_RESET_AFTER


async def search(client, json_query):
    """
    Executes a search on the anilist api.
    
    Parameters
    ----------
    client : ``Client``
        Client who received the source the event-
    json_query : `dict<str, object>`
        The query to execute.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    await RATE_LIMIT_LOCK.acquire()
    
    try:
        while True:
            async with client.http.post(
                'https://graphql.anilist.co',
                {CONTENT_TYPE: 'application/json'},
                data = to_json(json_query),
            ) as response:
                status_code = response.status
                if status_code == 200:
                    data = await response.json()
                    break
                
                if status_code == 400:
                    raw_data = await response.read()
                    await client.events.error(client, 'anilist.search', raw_data)
                    return abort('Something went wrong, please try again later.')
                
                if status_code == 429:
                    retry_after = response.headers.get(HEADER_RETRY_AFTER, None)
                    if (retry_after is None):
                        retry_after = 5
                    
                    await sleep(retry_after, KOKORO)
                    continue
                
                if status_code == 404:
                    return abort('Internal server error occurred, please try again later.')
                
                if status_code > 500:
                    return abort('Internal server error occurred, please try again later.')
                
                raw_data = await response.read()
                await client.events.error(
                    client,
                    'anilist.search',
                    f'{status_code!r} {response.headers!r} {raw_data}',
                )
                return abort(f'Something went wrong, please try again later.\nstatus = {status_code}')
            
    finally:
        KOKORO.call_after(RATE_LIMIT_RESET_AFTER, RATE_LIMIT_LOCK.release)
    
    return data
