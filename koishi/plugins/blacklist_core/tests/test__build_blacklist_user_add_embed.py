import vampytest
from hata import Embed, User

from ..builders import build_blacklist_user_add_embed


def _iter_options():
    user = User.precreate(202310170011, name = 'Reimu')
    
    yield (
        user,
        True,
        Embed(
            'Great success!',
            f'{user.full_name} has been blacklisted.',
        ).add_thumbnail(
            user.avatar_url,
        ),
    )

    yield (
        user,
        False,
        Embed(
            'Nice',
            f'{user.full_name} is already blacklisted.'
        ).add_thumbnail(
            user.avatar_url,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_blacklist_user_add_embed(user, success):
    """
    Tests whether ``build_blacklist_user_add_embed`` works as intended.
    
    Case: success.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        User to validate with.
    success : `bool`
        Whether they were added.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_blacklist_user_add_embed(user, success)
    vampytest.assert_instance(output, Embed)
    return output
