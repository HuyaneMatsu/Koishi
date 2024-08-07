import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..rendering import build_join_failed_embed_not_enough_users_to_start


def _iter_options():
    yield (
        Embed(
            'Ohoho',
            'There must be at least 1 other user in game to start it.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_failed_embed_not_enough_users_to_start():
    """
    Tests whether ``build_join_failed_embed_not_enough_users_to_start`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_join_failed_embed_not_enough_users_to_start()
    vampytest.assert_instance(output, Embed)
    return output
