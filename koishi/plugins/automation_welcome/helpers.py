__all__ = ()


def can_send_messages(channel, permissions):
    """
    Returns whether the user has permissions in the channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check in.
    permissions : ``Permission``
        The user's permissions there.
    
    Returns
    -------
    can_send_messages : `bool`
    """
    # send messages depends on channel type.
    if channel.is_in_group_thread():
        can_send_message = permissions.can_send_messages_in_threads
    else:
        can_send_message = permissions.can_send_messages
    return can_send_message
    
