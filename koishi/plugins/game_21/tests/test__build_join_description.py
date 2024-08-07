import vampytest
from hata import Guild, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..constants import GAME_21_EMOJI_ENTER
from ..rendering import build_join_description


def _iter_options():
    user_0 = User.precreate(202408010000, name = 'Mountain')
    user_1 = User.precreate(202408010001, name = 'of', display_name = 'Red')
    user_2 = User.precreate(202408010002, name = 'Faith')
    guild = Guild.precreate(202408010007)
    guild_profile_0 = GuildProfile(nick = 'Killed')
    guild_profile_2 = GuildProfile(nick = 'Dancehall')
    user_0.guild_profiles[guild.id] = guild_profile_0
    user_2.guild_profiles[guild.id] = guild_profile_2
    
    yield (
        [user_0],
        guild,
        1000,
        True,
        (
            f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
            f'Creator: {guild_profile_0.nick}\n'
            f'\n'
            f'Click on {GAME_21_EMOJI_ENTER} to join.'
        )
    )
    
    
    yield (
        [user_0],
        guild,
        1000,
        False,
        (
            f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
            f'Creator: {guild_profile_0.nick}'
        )
    )
    
    
    yield (
        [user_0, user_1],
        guild,
        1000,
        True,
        (
            f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
            f'Creator: {guild_profile_0.nick}\n'
            f'\n'
            f'Joined users:\n'
            f'{user_1.display_name}\n'
            f'\n'
            f'Click on {GAME_21_EMOJI_ENTER} to join.'
        )
    )
    
    
    yield (
        [user_0, user_1, user_2],
        guild,
        1000,
        True,
        (
            f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
            f'Creator: {guild_profile_0.nick}\n'
            f'\n'
            f'Joined users:\n'
            f'{user_1.display_name}\n'
            f'{guild_profile_2.nick}\n'
            f'\n'
            f'Click on {GAME_21_EMOJI_ENTER} to join.'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_description(users, guild, amount, ask_to_join):
    """
    Tests whether ``build_join_description`` works as intended.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    ask_to_join : `bool`
        Whether the embed should ask the users to join.
    
    Returns
    -------
    output : `str`
    """
    output = build_join_description(users, guild, amount, ask_to_join)
    vampytest.assert_instance(output, str)
    return output
