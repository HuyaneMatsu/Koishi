import vampytest
from hata import BUILTIN_EMOJIS, Emoji

from ..welcome_style import WelcomeStyle


def _assert_fields_set(welcome_style):
    """
    Asserts whether every attributes of the welcome style are set.
    
    Parameters
    ----------
    welcome_style : ``WelcomeStyle``
        The welcome style to check.
    """
    vampytest.assert_instance(welcome_style, WelcomeStyle)
    vampytest.assert_instance(welcome_style.button_contents, tuple)
    vampytest.assert_instance(welcome_style.button_emoji, Emoji)
    vampytest.assert_instance(welcome_style.images, tuple)
    vampytest.assert_instance(welcome_style.message_content_builders, tuple)
    vampytest.assert_instance(welcome_style.name, str)
    vampytest.assert_instance(welcome_style.reply_content_builders, tuple)


def test__WelcomeStyle__new():
    """
    Tests whether ``WelcomeStyle.__new__`` works as intended.
    """
    name = 'koishi'
    message_content_builders = (
        (lambda mention: 'content'),
    )
    images = (
        'image.png',
    )
    button_emoji = BUILTIN_EMOJIS['x']
    button_contents = (
        'satori',
    )
    reply_content_builders = (
        (lambda mention: 'hey mister'),
    )
    
    welcome_style = WelcomeStyle(
        name,
        message_content_builders,
        images,
        button_emoji,
        button_contents,
        reply_content_builders,
    )
    _assert_fields_set(welcome_style)
    
    vampytest.assert_eq(welcome_style.button_contents, button_contents)
    vampytest.assert_is(welcome_style.button_emoji, button_emoji)
    vampytest.assert_eq(welcome_style.images, images)
    vampytest.assert_eq(welcome_style.message_content_builders, message_content_builders)
    vampytest.assert_eq(welcome_style.name, name)
    vampytest.assert_eq(welcome_style.reply_content_builders, reply_content_builders)


def test__WelcomeStyle__repr():
    """
    Tests whether ``WelcomeStyle.__repr__`` works as intended.
    """
    name = 'koishi'
    message_content_builders = (
        (lambda mention: 'content'),
    )
    images = (
        'image.png',
    )
    button_emoji = BUILTIN_EMOJIS['x']
    button_contents = (
        'satori',
    )
    reply_content_builders = (
        (lambda mention: 'hey mister'),
    )
    
    welcome_style = WelcomeStyle(
        name,
        message_content_builders,
        images,
        button_emoji,
        button_contents,
        reply_content_builders,
    )
    
    vampytest.assert_instance(repr(welcome_style), str)
