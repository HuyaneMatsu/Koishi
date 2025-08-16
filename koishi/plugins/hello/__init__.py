from hata import Embed

from ...bot_utils.constants import COLOR__KOISHI_HELP
from ...bots import FEATURE_CLIENTS


USER_NAME_DEFAULT_0 = 'Alice'
USER_NAME_DEFAULT_1 = 'Marisa'


def build_hello_response(user_name_0, user_name_1):
    """
    Builds hello response.
    
    Parameters
    ----------
    user_name_0 : `str`
        User name to use.
    
    user_name_1 : `str`
        User name to use.
    
    Returns
    -------
    response : ``Embed``
    """
    return Embed(
        'Please don\'t just say "hello"',
        (
            f'Did someone just start a conversation by saying “Hello” or “Good Morning!” waiting for a response, '
            f'making you curios what they tried to tell you?\n'
            f'\n'
            f'**Is it wrong to start a conversation with a greeting?**\n'
            f'Yes and no.'
            f'- It is polite to start with an introduction.\n'
            f'- When you are saying just “Hello” and then wait for a response you either force the other person to '
            f'ignore your introduction or to ask back why you messaged them in the first place.\n'
            f'\n'
            f'Lets imagine {user_name_0} is Blendering, and then {user_name_1} asks them a question.\n'
            f'\n'
            f'> 5:14 **{user_name_1}:** Hey {user_name_0}, I have got a question!\n'
            f'> 5:16 **{user_name_0}:** Hello there {user_name_1}, tell me what is on your mind :3\n'
            f'> 5:30 **{user_name_1}:** [asks their question]\n'
            f'\n'
            f'In this example {user_name_0} is in deep blendering territory, '
            f'but when receives the message from {user_name_1}, '
            f'has to stop working and ask {user_name_1} how can they help. '
            f'Now {user_name_0} either gets back to work where they left of, '
            f'or waits till {user_name_1} types its message.\n'
            f'\n'
            f'> 5:14 **{user_name_1}:** Hey {user_name_0}, I was wondering how to import a model into Blender?\n'
            f'> 5:16 **{user_name_0}:** Hello there {user_name_1}, [...]\n'
            f'\n'
            f'Here are some things that went better this time:'
            f'- {user_name_1} Already finished typing its question, so {user_name_0} could instantly reply on it.\n'
            f'- {user_name_0} seen whether the question should be answered directly, or it can be postponed.'
        ),
        color = COLOR__KOISHI_HELP,
    )


def _user_name_priority_sort_key_getter(item):
    """
    Sort key getter used when sorting user names by preference.
    
    Parameters
    ----------
    item : `(str, (int, int))`
        Choices item.
    
    Returns
    -------
    sort_key : `(int, int)`
    """
    return item[1]


def get_user_names(interaction_event):
    """
    Get user names to example with.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    user_names : `(str, str)`
    """
    messages = interaction_event.channel.messages
    guild_id = interaction_event.guild_id
    interaction_user = interaction_event.user
    
    choices = {
        USER_NAME_DEFAULT_0 : (0, 1),
        USER_NAME_DEFAULT_1 : (0, 0),
        interaction_user.name_at(guild_id) : (1, 0),
    }
    
    if (messages is not None):
        for index, message in zip(range(9, -1, -1), reversed(messages)):
            user = message.author
            if (not user.bot) and (user is not interaction_user):
                choices.setdefault(user.name_at(guild_id), (3, index))
    
    choices = sorted(choices.items(), key = _user_name_priority_sort_key_getter, reverse = True)
    return choices[0][0], choices[1][0]


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True
)
async def hello(
    interaction_event,
):
    """
    Please don't just say "hello".
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``Embed``
    """
    return build_hello_response(*get_user_names(interaction_event))
