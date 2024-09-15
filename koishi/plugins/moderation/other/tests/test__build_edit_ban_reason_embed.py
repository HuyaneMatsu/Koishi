import vampytest
from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..edit_ban_reason import build_edit_ban_reason_embed


def _iter_options():
    user_id = 202409120000
    user_name = 'tenshi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        'hey mister',
        True,
        Embed(
            'Edit ban reason',
            f'**{user_name}**\'s ban reason has been edited.'
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Reason',
            (
                f'```\n'
                f'hey mister\n'
                f'```'
            ),
            inline = True,
        ),
    )
    
    yield (
        user,
        'hey sister',
        False,
        Embed(
            'Edit ban reason',
            f'**{user_name}** is **NOT YET** banned.'
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Reason',
            (
                f'```\n'
                f'hey sister\n'
                f'```'
            ),
            inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_edit_ban_reason_embed(user, reason, success):
    """
    Tests whether ``build_edit_ban_reason_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    reason : `None | str`
        Action reason.
    success : `bool`
        Whether the operation went through successfully.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_edit_ban_reason_embed(user, reason, success)
    vampytest.assert_instance(output, Embed)
    return output
