__all__ = ()

from hata import Client
from scarletio import to_coroutine

from ...bots import SLASH_CLIENT

from .operations import delete_automation_configuration_of


@SLASH_CLIENT.events
@to_coroutine
def guild_delete(client, guild, guild_profile):
    """
    handles a guild delete event. Removes the automation configuration for the given guild.
    Runs after other `guild_delete` handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The deleted guild.
    guild_profile : `None`, ``GuildProfile``
        The client's guild profile at the guild.
    """
    yield
    delete_automation_configuration_of(guild.id)

