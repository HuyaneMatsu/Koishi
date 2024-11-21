import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..easter_eggs.constants import COLOR_NAZRIN, IMAGE_URL_NAZRIN
from ..mute import build_mute_embed


def _iter_options():
    user_id = 202411170000
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        'hey mister',
        'great success',
        'because i said so',
        True,
        '2 weeks',
        True,
        Embed(
            'hey mister', 
            'great success',
            color = COLOR_NAZRIN,
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Duration',
            (
                '```\n'
                '2 weeks\n'
                '```'
            ),
            inline = True
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
            inline = True
        ).add_image(
            IMAGE_URL_NAZRIN,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mute_embed(user, title, description, reason, notify_user, duration_string, nazrin_mode):
    """
    Tests whether ``build_mute_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    title : `str`
        Embed title.
    description : `str`
        Embed description.
    reason : `None`, `str`
        Action reason.
    notify_user : `bool`
        Whether the user should be notified.
    duration_string : `str`
        The duration in string.
    nazrin_mode : `bool`
        Whether nazrin mode should be applied on the embed.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_mute_embed(user, title, description, reason, notify_user, duration_string, nazrin_mode)
    vampytest.assert_instance(output, Embed)
    return output
