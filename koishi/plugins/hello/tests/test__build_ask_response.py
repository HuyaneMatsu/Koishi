import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__KOISHI_HELP

from .. import build_hello_response


def test__build_hello_response():
    """
    Tests whether ``build_hello_response`` works as intended.
    """
    user_name_0 = 'Koishi'
    user_name_1 = 'Satori'
    
    output = build_hello_response(user_name_0, user_name_1)
    vampytest.assert_instance(output, Embed)
    
    vampytest.assert_eq(
        output,
            Embed(
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
                f'Here are some things that went better this time:\n'
                f'- {user_name_1} Already finished typing its question, so {user_name_0} could instantly reply on it.\n'
                f'- {user_name_0} seen whether the question should be answered directly, or it can be postponed.'
            ),
            color = COLOR__KOISHI_HELP,
        )
    )
