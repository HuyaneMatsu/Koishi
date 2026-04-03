import vampytest
from hata import Embed, User

from ..builders import build_blacklist_user_remove_embed


def _iter_options():
    user = User.precreate(202310170013, name = 'Reimu')
    
    yield (
        user,
        True,
        Embed(
            'WHAT!!!??',
            f'Why was {user.full_name} removed from blacklist??'
        ).add_thumbnail(
            user.avatar_url,
        ),
    )

    yield (
        user,
        False,
        Embed(
            'Okay',
            f'{user.full_name} was not blacklisted.'
        ).add_thumbnail(
            user.avatar_url,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_blacklist_user_remove_embed(user, success):
    """
    Tests whether ``build_blacklist_user_remove_embed`` works as intended.
    
    Case: success.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        User to validate with.
    success : `bool`
        Whether they were removed.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_blacklist_user_remove_embed(user, success)
    vampytest.assert_instance(output, Embed)
    return output
