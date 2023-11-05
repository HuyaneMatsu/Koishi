import vampytest
from hata import Message, MessageType, USER_MENTION_RP, User

from ..mention_mirror import mention_mirror_check_can_trigger, mention_replacer, mirror_mentions


def _iter_options__mention_replacer():
    user_0 = User.precreate(202311040000)
    user_1 = User.precreate(202311040001)
    
    yield {}, USER_MENTION_RP.fullmatch(user_0.mention), user_0.mention
    yield {str(user_0.id): user_1.mention}, USER_MENTION_RP.fullmatch(user_0.mention), user_1.mention


@vampytest._(vampytest.call_from(_iter_options__mention_replacer()).returning_last())
def test__mention_replacer(relations, match):
    """
    Tests whether ``mention_replacer`` works as intended.
    
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
    return mention_replacer(relations, match)


def _iter_options__mirror_mentions():
    user_0 = User.precreate(202311040002)
    user_1 = User.precreate(202311040003)
    user_2 = User.precreate(202311040004)
    
    yield user_0, user_1, 'hey mister', 'hey mister'
    yield (
        user_0,
        user_1,
        f'hey mister {user_0.mention} {user_1.mention} {user_2.mention}',
        f'hey mister {user_1.mention} {user_0.mention} {user_2.mention}',
    )
    
    yield (
        user_0,
        user_1,
        f'hey mister {user_0.mention} {user_0.mention}',
        f'hey mister {user_1.mention} {user_1.mention}',
    )


@vampytest._(vampytest.call_from(_iter_options__mirror_mentions()).returning_last())
def test__mirror_mentions(client, user, content):
    """
    Tests whether ``mirror_mentions`` works as intended.
    
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
    return mirror_mentions(client, user, content)


def _iter_options__mention_mirror_check_can_trigger():
    user_0 = User.precreate(202311040005)
    user_1 = User.precreate(202311040006)
    
    yield (
        user_0,
        Message.precreate(
            202311040007,
            content = None,
            mentioned_users = [user_0],
            message_type = MessageType.default,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040008,
            content = user_0.mention,
            mentioned_users = [],
            message_type = MessageType.default,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040009,
            content = user_0.mention,
            mentioned_users = [user_0],
            message_type = MessageType.inline_reply,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040010,
            content = user_0.mention,
            mentioned_users = [user_0],
            message_type = MessageType.default,
        ),
        user_0.mention,
    )

    yield (
        user_0,
        Message.precreate(
            202311040011,
            content = user_1.mention,
            mentioned_users = [user_1],
            message_type = MessageType.default,
        ),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__mention_mirror_check_can_trigger()).returning_last())
def test__mention_mirror_check_can_trigger(client, message):
    """
    Tests whether ``mention_mirror_check_can_trigger`` works as intended.
    
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
    return mention_mirror_check_can_trigger(client, message)
