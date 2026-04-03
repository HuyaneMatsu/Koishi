import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..un_mute import build_un_mute_embed


def _iter_options():
    user_id = 202601250303
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        0,
        'hey mister',
        'great success',
        'because i said so',
        True,
        Embed(
            'hey mister', 
            'great success',
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Notify user',
            (
                '```\n'
                'true\n'
                '```'
            ),
            inline = True
        ).add_field(
            'Reason',
            (
                '```\n'
                'because i said so\n'
                '```'
            ),
            inline = False
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_un_mute_embed(user, guild_id, title, description, reason, notify_user):
    """
    Tests whether ``build_un_mute_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    guild_id : `int`
        The local guild's identifier.
    
    title : `str`
        Embed title.
    
    description : `str`
        Embed description.
    
    reason : `None | str`
        Action reason.
    
    notify_user : `bool`
        Whether the user should be notified.
    
    orin_mode : `bool`
        Whether nazrin mode should be applied on the embed.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_un_mute_embed(user, guild_id, title, description, reason, notify_user)
    vampytest.assert_instance(output, Embed)
    return output
