import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..easter_eggs.constants import COLOR_ORIN, IMAGE_URL_ORIN
from ..kick import build_kick_embed


def _iter_options():
    user_id = 202601250301
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        0,
        'hey mister',
        'great success',
        'because i said so',
        True,
        True,
        Embed(
            'hey mister', 
            'great success',
            color = COLOR_ORIN,
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
        ).add_image(
            IMAGE_URL_ORIN,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_kick_embed(user, guild_id, title, description, reason, notify_user, orin_mode):
    """
    Tests whether ``build_kick_embed`` works as intended.
    
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
    output = build_kick_embed(user, guild_id, title, description, reason, notify_user, orin_mode)
    vampytest.assert_instance(output, Embed)
    return output
