import vampytest
from hata import Embed, User, GuildProfile

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ...balance_rendering import COLOR_CODE_RED, COLOR_CODE_RESET

from ..embed_builders import build_success_embed


def _iter_options():
    guild_id = 202507110005
    user = User.precreate(202507110004, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        user,
        guild_id,
        1000,
        100,
        Embed(
            'Amazing, Awesome, Superb!!',
            f'You took away from Sato 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_field(
            f'Their {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'1000 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 900\n'
                f'```'
            ),
            inline = True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed(target_user, guild_id, down_from, amount):
    """
    Tests whether ``build_success_embed`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    down_from : `int`
        From what amount the user is up from.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed(target_user, guild_id, down_from, amount)
    vampytest.assert_instance(output, Embed)
    return output
