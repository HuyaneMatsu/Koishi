__all__ = ()

from hata.ext.slash import abort


def check_user_permissions(event):
    """
    Checks whether the user has permission to use this command.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    """
    if not event.user_permissions.administrator:
        abort('You must have administrator permission to use this command.')


def default_channel_and_check_its_guild(event, channel):
    """
    Defaults the selected channel
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel``
        The selected channel
    
    Returns
    -------
    channel : ``Channel``
    """
    if channel is None:
        channel = event.channel
    
    if channel.guild_id != event.guild_id:
        abort('The selected channel\'s guild is from an other guild.')
    
    return channel


def check_channel_and_client_permissions(client, channel):
    """
    Checks the channel and the client's permissions in it.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The channel to log into.
    """
    if not channel.is_in_group_guild_system():
        abort('Please select a guild system channel.')
    
    if not channel.cached_permissions_for(client).send_messages:
        abort('I cannot send messages into the selected channel.')
