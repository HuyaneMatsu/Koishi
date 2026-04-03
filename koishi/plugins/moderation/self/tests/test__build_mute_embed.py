import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..mute import build_mute_embed


def _iter_options():
    user_id = 202601250308
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        0,
        'hey mister',
        'great success',
        'because i said so',
        '2 weeks',
        Embed(
            'hey mister', 
            'great success',
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Duration',
            (
                '```\n'
                '2 weeks\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Reason',
            (
                '```\n'
                'because i said so\n'
                '```'
            ),
            inline = False,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mute_embed(user, guild_id, title, description, reason, duration_string):
    """
    Tests whether ``build_mute_embed`` works as intended.
    
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
    
    duration_string : `str`
        The duration in string.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_mute_embed(user, guild_id, title, description, reason, duration_string)
    vampytest.assert_instance(output, Embed)
    return output
