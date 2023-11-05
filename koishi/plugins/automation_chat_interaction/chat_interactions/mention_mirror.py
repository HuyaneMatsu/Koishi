__all__ = ()

from functools import partial as partial_func

from hata import MessageType, USER_MENTION_RP

from ..chat_interaction import ChatInteraction


NAME = 'mention mirror'


def mention_replacer(relations, match):
    """
    Returns a new mention for the given match.
    
    Parameters
    ----------
    relations : `dict<str, str>`
        Mention relations to apply.
    match : `re.Match`
        The matched mention.
    
    Returns
    -------
    mention : `str`
    """
    matched_id = match.group(1)
    mention = relations.get(matched_id, None)
    if mention is None:
        mention = match.group(0)
    
    return mention


def mirror_mentions(client, user, content):
    """
    Mirrors mentions in the given content.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        Client to mirror its permissions.
    user : ``ClientUserBase``
        The user to mirror the permissions with.
    content : `str`
        The content to mirror the mentions in.
    
    Returns
    -------
    content : `str`
    """
    relations = {
        str(client.id): user.mention,
        str(user.id): client.mention,
    }
    
    return USER_MENTION_RP.sub(partial_func(mention_replacer, relations), content)


def mention_mirror_check_can_trigger(client, message):
    """
    Returns whether the chat interaction can be triggered.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the message.
    message : ``Message``
        The received message.
    
    Returns
    -------
    outcome : `None | str`
    """
    content = message.content
    if content is None:
        return None
    
    if message.type is not MessageType.default:
        return None
    
    mentioned_users = message.mentioned_users
    if (mentioned_users is None) or (client not in mentioned_users):
        return None
    
    return content
    

async def mention_mirror_trigger(client, message, outcome):
    """
    Triggers the chat interaction.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    message : ``Message``
        The received message.
    outcome : `str`
        Output of the can trigger check.
    """
    user = message.author
    content = mirror_mentions(client, user, outcome)
    await client.message_create(message.channel, allowed_mentions = [user], content = content)


CHAT_INTERACTION = ChatInteraction(
    NAME,
    mention_mirror_check_can_trigger,
    mention_mirror_trigger,
)
