from hata import Embed

from ...bot_utils.constants import COLOR__KOISHI_HELP
from ...bots import FEATURE_CLIENTS


def build_ask_response():
    """
    Builds ask response.
    
    Returns
    -------
    response : ``Embed``
    """
    return Embed(
        'How to ask?',
        (
            'Don\'t ask to ask just ask.\n'
            '\n'
            '- You will have much higher chances of getting an answer.\n'
            '- It saves time both for us and you as we can skip the whole process of actually getting the question '
            'out of you.\n'
            '- While putting the question into words you have a high chance of answering your own question.'
        ),
        color = COLOR__KOISHI_HELP,
    )


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True
)
async def ask():
    """
    How to ask!
    
    This function is a coroutine.
    
    Returns
    -------
    response : ``Embed``
    """
    return build_ask_response()
