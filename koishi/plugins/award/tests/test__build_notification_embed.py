import vampytest
from hata import Embed, User, GuildProfile

from ....bot_utils.constants import COLOR__GAMBLING

from ...balance_rendering import COLOR_CODE_GREEN, COLOR_CODE_RESET

from ..embed_builders import build_notification_embed


def _iter_options():
    guild_id = 202507110003
    user = User.precreate(202507110002, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        user,
        guild_id,
        1000,
        100,
        'streak',
        'Love you!',
        Embed(
            'Amazing, Awesome, Superb!!',
            'You have been awarded by Sato with 100 streak.',
            color = COLOR__GAMBLING,
        ).add_field(
            'Your streak',
            (
                f'```ansi\n'
                f'1000 {COLOR_CODE_GREEN}->{COLOR_CODE_RESET} 1100\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Message:',
            'Love you!',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed(source_user, guild_id, up_from, amount, awarded_with, message):
    """
    Tests whether ``build_notification_embed`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    up_from : `int`
        From what amount the user is up from.
    
    awarded_with : `str`
        With what the user is awarded with.
    
    message : `None | str`
        Additional message.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_notification_embed(source_user, guild_id, up_from, amount, awarded_with, message)
    vampytest.assert_instance(output, Embed)
    return output
