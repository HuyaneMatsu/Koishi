import vampytest
from hata import Embed, Guild, GuildProfile, InteractionEvent, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import CARD_NUMBERS, CARD_TYPES
from ..player import Player
from ..rendering import build_end_embed_multi_player
from ..session import Game21Session


def _iter_options():
    session_id = 13333
    user_0 = User.precreate(202408060003, name = 'Remilia')
    user_1 = User.precreate(202408060004, name = 'Sakuya')
    guild = Guild.precreate(202408060005)
    guild_profile_1 = GuildProfile(nick = 'Suyu')
    user_1.guild_profiles[guild.id] = guild_profile_1
    
    player_0 = Player(user_0, InteractionEvent.precreate(202408060006))
    player_0.hand.add_card(8)
    player_1 = Player(user_1, InteractionEvent.precreate(202408060007))
    player_1.hand.add_card(6)
    
    session = Game21Session(session_id, guild, 1000, InteractionEvent.precreate(202408060008))
    
    yield (
        session,
        [player_0, player_1],
        None,
        [player_0, player_1],
        Embed(
            'Game ended',
            f'Total bet amount: {2000!s} {EMOJI__HEART_CURRENCY}',
            color = COLOR__GAMBLING,
        ).add_field(
            'Draw',
            (
                f'{user_0.name}\n'
                f'{guild_profile_1.nick}'
            ),
        ).add_field(
            (
                f'{user_0.name}\'s\n'
                f'cards\' weight: {player_0.hand.total!s}'
            ),
            f'Round 1: {CARD_TYPES[0]} {CARD_NUMBERS[8]}',
            inline = True,
        ).add_field(
            (
                f'{guild_profile_1.nick}\'s\n'
                f'cards\' weight: {player_1.hand.total!s}'
            ),
            f'Round 1: {CARD_TYPES[0]} {CARD_NUMBERS[6]}',
            inline = True,
        )
    )
    
    yield (
        session,
        [player_0, player_1],
        [player_1],
        [player_0],
        Embed(
            'Game ended',
            f'Total bet amount: {2000!s} {EMOJI__HEART_CURRENCY}',
            color = COLOR__GAMBLING,
        ).add_field(
            'Winners',
            f'{guild_profile_1.nick}',
        ).add_field(
            'Losers',
            f'{user_0.name}',
        ).add_field(
            (
                f'{user_0.name}\'s\n'
                f'cards\' weight: {player_0.hand.total!s}'
            ),
            f'Round 1: {CARD_TYPES[0]} {CARD_NUMBERS[8]}',
            inline = True,
        ).add_field(
            (
                f'{guild_profile_1.nick}\'s\n'
                f'cards\' weight: {player_1.hand.total!s}'
            ),
            f'Round 1: {CARD_TYPES[0]} {CARD_NUMBERS[6]}',
            inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_end_embed_multi_player(session, players, winners, losers):
    """
    Tests whether ``build_end_embed_multi_player`` works as intended.

    Parameters
    ----------
    session : ``Game21Session``
        Game session.
    players : `list<Player>`
        All player.
    winners : `None | list<Player>`
        Winning players.
    losers : `None | list<Player>`
        Losing players.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_end_embed_multi_player(session, players, winners, losers)
    vampytest.assert_instance(output, Embed)
    return output
