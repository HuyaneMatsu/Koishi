__all__ = ('Nue',)

from hata import Client, IconType, IntentFlag, Status

import config


Nue = Client(
    config.NUE_TOKEN,
    client_id = config.NUE_ID,
    status = Status.online,
    should_request_users = False,
    intents = IntentFlag().update_by_keys(), # no changes
    application_id = config.NUE_ID,
    extensions = ('slash',),
)


@Nue.events
async def user_update(client, user, old_attributes):
    """
    Handles user update events.
    If Nue's avatar was changed then updates the Nue bot's.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    user : ``ClientUserBase``
        The user who was updated.
    
    old_attributes : `None | dict<str, object>`
        The changed attributes if known.
    """
    if user.id != 626800301118062592:
        return
    
    # Do nothing if avatar did not change
    if (old_attributes is not None) and ('avatar' not in old_attributes.keys()):
        return
    
    # Skip if nue has default avatar
    if user.avatar_type is IconType.none:
        return
    
    async with client.http.get(user.avatar_url_as(size = 4096)) as response:
        if response.status != 200:
            return
        
        data = await response.read()
    
    await client.edit(avatar = data)
    await client.application_edit_own(icon = data)
