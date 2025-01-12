import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..rendering import build_join_failed_embed_not_enough_hearts


def _iter_options():
    yield (
        2000,
        1000,
        False,
        Embed(
            'Ohoho',
            (
                f'You must have at least {2000!s} available {EMOJI__HEART_CURRENCY} to join.\n'
                f'You have {1000!s} {EMOJI__HEART_CURRENCY}.'
            ),
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        2000,
        1000,
        True,
        Embed(
            'Oh snap!',
            (
                f'I must have at least {2000!s} available {EMOJI__HEART_CURRENCY} to join.\n'
                f'I have {1000!s} {EMOJI__HEART_CURRENCY}.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_failed_embed_not_enough_hearts(expected, available, me):
    """
    Tests whether ``build_join_failed_embed_not_enough_hearts`` works as intended.
    
    Parameters
    ----------
    expected : `int`
        The expected hearts to have.
    
    available : `int`
        The available hearts of a user.
    
    me : `bool`
        Whether the client is checking itself.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_join_failed_embed_not_enough_hearts(expected, available, me)
    vampytest.assert_instance(output, Embed)
    return output
