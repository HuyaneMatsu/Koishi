import vampytest
from hata import Embed, Guild, GuildProfile, InteractionEvent, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_building import build_daily_embed_extended


def _iter_options():
    user = User.precreate(202412030034, name = 'koishi')
    guild = Guild.precreate(202412030035, users = [user])
    user.guild_profiles[guild.id] = GuildProfile(nick = 'satori')
    
    yield (
        InteractionEvent.precreate(
            202412030036,
            user = user,
            guild = guild,
        ),
        user,
        20,
        12,
        True,
        Embed(
            f'You have 20 {EMOJI__HEART_CURRENCY}',
            'You are on a 12 day streak, and you are ready to claim your daily!',
            color = COLOR__GAMBLING,
        ).add_field(        
            'Daily reward calculation:',
            (
                '**Base:**\n'
                'Base: 100\n'
                'Extra limit: 300\n'
                'Extra per streak: 5\n'
                '\n'
                '**Formula:**\n'
                'base + min(extra\\_limit, extra\\_per\\_streak * streak) + streak\n'
                '100 + min(300, 5 * 12) + 12 = 172'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_daily_embed_extended(interaction_event, target_user, balance, streak, ready_to_claim):
    """
    Tests whether ``build_daily_embed_extended`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    ready_to_claim : `bool`
        Whether the user is ready to claim their daily.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_daily_embed_extended(interaction_event, target_user, balance, streak, ready_to_claim)
    vampytest.assert_instance(output, Embed)
    return output
