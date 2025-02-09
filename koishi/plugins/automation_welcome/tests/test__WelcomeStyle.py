import vampytest
from hata import BUILTIN_EMOJIS

from ..welcome_style_reply import WelcomeStyleReply
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
    vampytest.assert_instance(welcome_style.client_id, int)
    vampytest.assert_instance(welcome_style.images, tuple)
    vampytest.assert_instance(welcome_style.image_creator, str)
    vampytest.assert_instance(welcome_style.message_content_builders, tuple)
    vampytest.assert_instance(welcome_style.name, str)
    vampytest.assert_instance(welcome_style.reply_styles, tuple)


def test__WelcomeStyle__new():
    """
    Tests whether ``WelcomeStyle.__new__`` works as intended.
    """
    name = 'koishi'
    client_id = 202502080005
    message_content_builders = (
        (lambda target: 'content'),
    )
    images = (
        'image.png',
    )
    image_creator = 'remilia'
    reply_styles = (
        WelcomeStyleReply(
            'Stare at them',
            BUILTIN_EMOJIS['heart'],
            (lambda source, target: f'{source} stares at {target}'),
        ),
    )
    
    welcome_style = WelcomeStyle(
        name,
        client_id,
        message_content_builders,
        images,
        image_creator,
        reply_styles,
    )
    _assert_fields_set(welcome_style)
    
    vampytest.assert_eq(welcome_style.client_id, client_id)
    vampytest.assert_eq(welcome_style.images, images)
    vampytest.assert_eq(welcome_style.image_creator, image_creator)
    vampytest.assert_eq(welcome_style.message_content_builders, message_content_builders)
    vampytest.assert_eq(welcome_style.name, name)
    vampytest.assert_eq(welcome_style.reply_styles, reply_styles)


def test__WelcomeStyle__repr():
    """
    Tests whether ``WelcomeStyle.__repr__`` works as intended.
    """
    name = 'koishi'
    client_id = 202502080006
    message_content_builders = (
        (lambda target: 'content'),
    )
    images = (
        'image.png',
    )
    image_creator = 'remilia'
    reply_styles = (
        WelcomeStyleReply(
            'Stare at them',
            BUILTIN_EMOJIS['heart'],
            (lambda source, target: f'{source} stares at {target}'),
        ),
    )
    
    welcome_style = WelcomeStyle(
        name,
        client_id,
        message_content_builders,
        images,
        image_creator,
        reply_styles,
    )
    
    vampytest.assert_instance(repr(welcome_style), str)
