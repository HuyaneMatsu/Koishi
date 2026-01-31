import vampytest

from ..welcome_image import WelcomeImage


def _assert_fields_set(welcome_image):
    """
    Asserts whether every attributes of the welcome image are set.
    
    Parameters
    ----------
    welcome_image : ``WelcomeImage``
        The welcome image to check.
    """
    vampytest.assert_instance(welcome_image, WelcomeImage)
    vampytest.assert_instance(welcome_image.creator, str)
    vampytest.assert_instance(welcome_image.url, str)


def test__WelcomeImage__new():
    """
    Tests whether ``WelcomeImage.__new__`` works as intended.
    """
    creator = 'koishi'
    url = 'https://orindance.party/'
    
    welcome_image = WelcomeImage(
        creator,
        url,
    )
    _assert_fields_set(welcome_image)
    
    vampytest.assert_eq(welcome_image.creator, creator)
    vampytest.assert_eq(welcome_image.url, url)


def test__WelcomeImage__repr():
    """
    Tests whether ``WelcomeImage.__repr__`` works as intended.
    """
    creator = 'koishi'
    url = 'https://orindance.party/'
    
    welcome_image = WelcomeImage(
        creator,
        url,
    )
    
    output = repr(welcome_image)
    vampytest.assert_instance(output, str)
