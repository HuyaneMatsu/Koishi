from collections import deque as Deque

import vampytest

from hata import Channel, InteractionEvent, User, Message
from hata.discord.channel.message_history import MessageHistory

from .. import USER_NAME_DEFAULT_0, USER_NAME_DEFAULT_1, get_user_names


def _iter_options():
    user_0 = User.precreate(202507120020, name = USER_NAME_DEFAULT_0)
    user_1 = User.precreate(202507120022, name = 'Satori')
    user_2 = User.precreate(202507120025, name = 'Nue')
    user_3 = User.precreate(202507120026, name = 'Chimi')
    
    channel_0 = Channel.precreate(202507120021)
    
    channel_1 = Channel.precreate(202507120027)
    channel_1._message_history = MessageHistory(10)
    channel_1._message_history.messages = Deque(
        [
            Message.precreate(202507120028, author = user_2,),
            Message.precreate(202507120029, author = user_2),
            Message.precreate(202507120030, author = user_1),
            Message.precreate(202507120031, author = user_3),
            Message.precreate(202507120032, author = user_2),
        ],
        10,
    )
    
    yield (
        InteractionEvent.precreate(
            202507120023,
            user = user_0,
            channel = channel_0,
        ),
        (
            USER_NAME_DEFAULT_0,
            USER_NAME_DEFAULT_1,
        ),
    )
    
    yield (
        InteractionEvent.precreate(
            202507120024,
            user = user_1,
            channel = channel_0,
        ),
        (
            user_1.name,
            USER_NAME_DEFAULT_0,
        ),
    )
    
    yield (
        InteractionEvent.precreate(
            202507120033,
            user = user_1,
            channel = channel_1,
        ),
        (
            user_2.name,
            user_3.name,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_names(interaction_event):
    """
    Get user names to example with.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `(str, str)`
    """
    output = get_user_names(interaction_event)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], str)
    vampytest.assert_instance(output[1], str)
    return output
