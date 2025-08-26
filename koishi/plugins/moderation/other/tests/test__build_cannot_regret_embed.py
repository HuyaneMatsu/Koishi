import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ..helpers import build_cannot_regret_embed


def _iter_options():
    user_id = 202508260000
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        0,
        'because i said so',
        'kicking',
        Embed(
            'Denied',
            (
                'You cannot regret kicking **mayumi**.\n'
                'Was the action different, or is it is already too late?!'
            ),
        ).add_field(
            'Reason',
            (
                '```\n'
                'because i said so\n'
                '```'
            ),
            inline = False
        )
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_cannot_regret_embed(user, guild_id, reason, action):
    """
    Tests whether ``build_cannot_regret_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `str`
        Regret-ban reason.
    
    action : `str`
        The action's name within its `-ed` form.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_cannot_regret_embed(user, guild_id, reason, action)
    vampytest.assert_instance(output, Embed)
    return output
