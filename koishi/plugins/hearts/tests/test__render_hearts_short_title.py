import vampytest
from hata import Guild, GuildProfile, InteractionEvent, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..rendering import render_hearts_short_title


def _iter_options():
    user_0 = User.precreate(202412030010, name = 'koishi')
    user_1 = User.precreate(202412030011, name = 'orin')
    guild = Guild.precreate(202412030012, users = [user_0])
    user_0.guild_profiles[guild.id] = GuildProfile(nick = 'satori')
    
    yield (
        InteractionEvent.precreate(
            202412030012,
            user = user_0,
            guild = guild,
        ),
        user_0,
        20,
        f'You have 20 {EMOJI__HEART_CURRENCY}'
    )
    
    yield (
        InteractionEvent.precreate(
            202412030012,
            user = user_1,
            guild = guild,
        ),
        user_0,
        20,
        f'satori has 20 {EMOJI__HEART_CURRENCY}'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_hearts_short_title(interaction_event, target_user, total):
    """
    Tests whether ``render_hearts_short_title`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    total : `int`
        The user's total hearts.
    
    Returns
    -------
    output : `str`
    """
    output = render_hearts_short_title(interaction_event, target_user, total)
    vampytest.assert_instance(output, str)
    return output
