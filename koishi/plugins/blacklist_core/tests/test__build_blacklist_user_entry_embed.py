import vampytest
from hata import Embed, User

from ..builders import build_blacklist_user_entry_embed


def _iter_options():
    user = User.precreate(202310170012, name = 'Reimu')
    
    yield (
        user,
        True,
        Embed(
            'Nice!',
            f'{user.full_name} is blacklisted.'
        ).add_thumbnail(
            user.avatar_url,
        ),
    )

    yield (
        user,
        False,
        Embed(
            'Uoh',
            f'{user.full_name} is **NOT YET** blacklisted.'
        ).add_thumbnail(
            user.avatar_url,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_blacklist_user_entry_embed(user, blacklisted):
    """
    Tests whether ``build_blacklist_user_entry_embed`` works as intended.
    
    Case: success.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        User to validate with.
    success : `bool`
        Whether they are blacklisted.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_blacklist_user_entry_embed(user, blacklisted)
    vampytest.assert_instance(output, Embed)
    return output
