import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__KOISHI_HELP

from .. import build_ask_response


def test__build_ask_response():
    """
    Tests whether ``build_ask_response`` works as intended.
    """
    output = build_ask_response()
    vampytest.assert_instance(output, Embed)
    
    vampytest.assert_eq(
        output,
        Embed(
            'How to ask?',
            (
                'Don\'t ask to ask just ask.\n'
                '\n'
                '- You will have much higher chances of getting an answer.\n'
                '- It saves time both for us and you as we can skip the whole process of actually getting the '
                'question out of you.\n'
                '- While putting the question into words you have a high chance of answering your own question.'
            ),
            color = COLOR__KOISHI_HELP,
        )
    )
