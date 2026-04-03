__all__ = ('schedule_image_refresh',)

from scarletio import CancelledError, Task
from hata import KOKORO, DiscordException, ERROR_CODES


REFRESH_AFTER = 5.0
RETRY_MAX = 2


def schedule_image_refresh(client, message, interaction_event = None):
    """
    Schedules image refresh if required.
    
    Parameters
    ----------
    client : ``Client``
        Client to call refresh with.
    message : ``None | Message``
        The message to refresh.
    interaction_event : `None | InteractionEvent` = `None`, Optional
        Interaction event to refresh with if applicable.
    """
    if _should_image_refresh(message):
        KOKORO.call_after(REFRESH_AFTER, _invoke_image_refresh, client, message, interaction_event)


def _should_image_refresh(message):
    """
    Returns whether the message's embed's image should be refreshed.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
    
    Returns
    -------
    should_image_refresh : `bool`
    """
    if message is None:
        return False
    
    embed = message.embed
    if embed is None:
        return False
    
    image = embed.image
    if image is None:
        return False
    
    if image.width and image.height:
        return False
    
    return True


def _invoke_image_refresh(client, message, interaction_event, retry = 0):
    """
    Invokes refresh is required.
    
    Parameters
    ----------
    client : ``Client``
        Client to call refresh with.
    message : ``Message``
        The message to refresh.
    interaction_event : `None | InteractionEvent`
        Interaction event to refresh with if applicable.
    """
    if _should_image_refresh(message) and retry < RETRY_MAX:
        Task(KOKORO, _image_refresh(client, message, interaction_event, retry + 1))


async def _image_refresh(client, message, interaction_event, retry):
    """
    Refreshes the image.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client to call refresh with.
    message : ``Message``
        The message to refresh.
    interaction_event : `None | InteractionEvent`
        Interaction event to refresh with if applicable.
    """
    if (interaction_event is not None):
        # if the interaction client is not in the guild we are not receiving
        if not interaction_event.application_permissions.view_channel:
            try:
                await client.interaction_followup_message_get(interaction_event, message)
            except GeneratorExit:
                raise
            
            except CancelledError:
                raise
            
            except ConnectionError:
                return
            
            except DiscordException as exception:
                if exception.code == ERROR_CODES.unknown_message: # message deleted
                    return
                
                raise
            
            if not _should_image_refresh(message):
                return
        
        try:
            await client.interaction_followup_message_edit(
                interaction_event,
                message,
                embed = message.embed
            )
        except (GeneratorExit, CancelledError):
            raise
        
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ):
                return
            
            if exception.code != ERROR_CODES.unknown_interaction: # interaction expired
                await client.events.error(client, '_image_refresh', exception)
                return
        
        except BaseException as exception:
            await client.events.error(client, '_image_refresh', exception)
            return
        
        else:
            _invoke_image_refresh(client, message, interaction_event, retry)
            return
    
    if not message.channel.cached_permissions_for(client).view_channel:
        return
    
    try:
        await client.message_edit(message, embed = message.embed)
    except (GeneratorExit, CancelledError):
        raise
    
    except ConnectionError:
        return

    except DiscordException as exception:
        if exception.code in (
            ERROR_CODES.unknown_message, # message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            return
        
        await client.events.error(client, '_image_refresh', exception)
        return
    
    except BaseException as exception:
        await client.events.error(client, '_image_refresh', exception)
        return
    
    else:
        _invoke_image_refresh(client, message, interaction_event, retry)
        return
