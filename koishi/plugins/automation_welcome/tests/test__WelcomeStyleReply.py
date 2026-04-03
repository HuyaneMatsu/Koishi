from types import FunctionType

import vampytest
from hata import BUILTIN_EMOJIS, Emoji

from ..welcome_style_reply import WelcomeStyleReply


def _assert_fields_set(reply_style):
    """
    Asserts whether every fields are set of the given reply style.
    
    Parameters
    ----------
    reply_style : ``WelcomeStyleReply``
        The reply style to test.
    """
    vampytest.assert_instance(reply_style, WelcomeStyleReply)
    vampytest.assert_instance(reply_style.button_content, str)
    vampytest.assert_instance(reply_style.button_emoji, Emoji)
    vampytest.assert_instance(reply_style.reply_content_builder, FunctionType)


def test__WelcomeStyleReply__new():
    """
    Tests whether ``WelcomeStyleReply.__new__`` works as intended.
    """
    button_content = 'Call them!'
    button_emoji = BUILTIN_EMOJIS['x']
    reply_content_builder = lambda source, target: f'{source} calls {target}.'
    
    reply_style = WelcomeStyleReply(button_content, button_emoji, reply_content_builder)
    _assert_fields_set(reply_style)
    vampytest.assert_eq(reply_style.button_content, button_content)
    vampytest.assert_is(reply_style.button_emoji, button_emoji)
    vampytest.assert_is(reply_style.reply_content_builder, reply_content_builder)


def test__WelcomeStyleReply__repr():
    """
    Tests whether ``WelcomeStyleReply.__repr__`` works as intended.
    """
    button_content = 'Call them!'
    button_emoji = BUILTIN_EMOJIS['x']
    reply_content_builder = lambda source, target: f'{source} calls {target}.'
    
    reply_style = WelcomeStyleReply(button_content, button_emoji, reply_content_builder)
    
    vampytest.assert_instance(repr(reply_style), str)
