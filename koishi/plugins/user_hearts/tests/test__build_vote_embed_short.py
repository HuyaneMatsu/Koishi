import vampytest
from hata import Embed, Guild, GuildProfile, InteractionEvent, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_building import build_vote_embed_short


def _iter_options():
    user = User.precreate(202412030040, name = 'koishi')
    guild = Guild.precreate(202412030041, users = [user])
    user.guild_profiles[guild.id] = GuildProfile(nick = 'satori')
    
    yield (
        InteractionEvent.precreate(
            202412030042,
            user = user,
            guild = guild,
        ),
        user,
        20,
        12,
        True,
        Embed(
            f'You have 20 {EMOJI__HEART_CURRENCY}',
            'You are on a 12 day streak, and you are ready to vote!',
            color = COLOR__GAMBLING,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_vote_embed_short(interaction_event, target_user, balance, streak, ready_to_vote):
    """
    Tests whether ``build_vote_embed_short`` works as intended.
    
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
    
    ready_to_vote : `bool`
        Whether the user is ready to vote.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_vote_embed_short(interaction_event, target_user, balance, streak, ready_to_vote)
    vampytest.assert_instance(output, Embed)
    return output
