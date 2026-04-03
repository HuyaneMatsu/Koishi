__all__ = ('apply_mode_nazrin', 'should_show_nazrin',)

from random import random

from .constants import COLOR_NAZRIN, IMAGE_URL_NAZRIN , TIMEOUT_DURATION_MIN_NAZRIN


def apply_mode_nazrin(embed):
    """
    Applies nazrin mode to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to nazrinify.
    """
    embed.add_image(IMAGE_URL_NAZRIN)
    embed.color = COLOR_NAZRIN


def should_show_nazrin(duration):
    """
    Returns whether Nazrin silencing Kyouko image should be shown.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Timeout duration.
    
    Returns
    -------
    should_show_nazrin : `bool`
    """
    return duration >= TIMEOUT_DURATION_MIN_NAZRIN and random() > 0.5
