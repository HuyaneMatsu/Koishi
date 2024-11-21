__all__ = ()

from hata.ext.slash import abort


def check_move_permissions(client, event, target_channel, require_admin_permissions):
    """
    Checks the user's permissions whether the user can move messages.
    
    Parameters
    ----------
    client : ``Client``
        The respective client who is moving the messages.
    event : ``InteractionEvent``
        The received interaction event.
    target_channel : ``Channel``
        The target channel of moving.
    require_admin_permissions : `bool`
        Whether we should require admin permission and not manage messages.
    """
    return check_move_permissions_custom(
        client, event.channel, target_channel, event.user_permissions, require_admin_permissions
    )


def check_move_permissions_custom(client, source_channel, target_channel, user_permissions, require_admin_permissions):
    """
    Checks the user's permissions whether the user can move messages. This is a more customizable checker than 
    ``.check_move_permissions``, since it directly accepts context parameters.
    
    Parameters
    ----------
    client : ``Client``
        The respective client who is moving the messages.
    source_channel : ``Channel``
        Source channel to move from.
    target_channel : ``Channel``
        The target channel of moving.
    user_permissions : ``Permission``
        The user's permissions.
    require_admin_permissions : `bool`
        Whether we should require admin permission and not manage messages.
    """
    if require_admin_permissions:
        if (not user_permissions.administrator):
            return abort('You need to have administrator permission to invoke this command.')
    
    else:
        if (not user_permissions.manage_messages):
            return abort('You need to have manage messages permission to invoke this command.')
        
        if (source_channel is None) or (not source_channel.cached_permissions_for(client).manage_messages):
            return abort('I require manage messages permission in this channel to execute the command.')
        
    if (not target_channel.cached_permissions_for(client).manage_webhooks):
        return abort('I need manage webhook permission in the target channel to execute this this command.')
