__all__ = ()

from hata import Permission

from ..blacklist_core import is_user_id_in_blacklist


PERMISSION_MASK_MESSAGING_DEFAULT = Permission().update_by_keys(send_messages = True)
PERMISSION_MASK_MESSAGING_THREAD = Permission().update_by_keys(send_messages_in_threads = True)


def is_vote_valid(channel, user, mask):
    """
    Returns whether the user's vote is valid.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel where the action was executed.
    user : ``ClientUserBase``
        The user to check.
    mask : `bool`
        Permission mask that have to be satisfied.
    
    Returns
    -------
    is_vote_valid : `bool`
    """
    if user.bot:
        return False
    
    if is_user_id_in_blacklist(user.id):
        return False
    
    if channel.permissions_for(user) & mask != mask:
        return False
    
    return True


async def get_voters(client, message, emoji_id):
    """
    Gets all the votes for the given `emoji_id`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to do requests with if applicable.
    message : ``Message``
        The message to scan.
    emoji_id : `int`
        The emoji's identifier to scan for.
    
    Returns
    -------
    voters : `set<ClientUserBase>`
    """
    if not emoji_id:
        return set()
    
    reactions = message.reactions
    if reactions is None:
        # Should not happen
        return set()
    
    reactions = [reaction for reaction in reactions.iter_reactions() if reaction.emoji.id == emoji_id]
    
    channel = message.channel
    if channel.is_in_group_thread():
        mask = PERMISSION_MASK_MESSAGING_THREAD
    else:
        mask = PERMISSION_MASK_MESSAGING_DEFAULT
    
    voters = set()
    
    for reaction in reactions:
        users = await client.reaction_user_get_all(message, reaction)
        for user in users:
            if is_vote_valid(channel, user, mask):
                voters.add(user)
    
    return voters
