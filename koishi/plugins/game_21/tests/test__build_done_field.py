import vampytest
from hata import Embed, Guild, GuildProfile, User

from ..constants import ACE_INDEX, CARD_NUMBERS, CARD_TYPES
from ..hand import Hand
from ..rendering import add_done_field


def _iter_options():
    hand = Hand()
    user = User.precreate(202408020000)
    guild = Guild.precreate(202408020001)
    guild_profile = GuildProfile(nick = 'hey')
    user.guild_profiles[guild.id] = guild_profile
    
    yield (
        Embed(),
        user,
        guild,
        hand,
        Embed().add_field(
            (
                f'{guild_profile.nick}\'s\n'
                f'cards\' weight: {hand.total!s}'
            ),
            (
                '_ _'
            ),
            inline = True,
        )
    )
    
    hand = Hand()
    hand.add_card(len(CARD_NUMBERS) + 8)
    hand.add_card(ACE_INDEX)
    
    yield (
        Embed(),
        user,
        guild,
        hand,
        Embed().add_field(
            (
                f'{guild_profile.nick}\'s\n'
                f'cards\' weight: {hand.total!s}'
            ),
            (
                f'Round 1: {CARD_TYPES[1]} {CARD_NUMBERS[8]}\n'
                f'Round 2: {CARD_TYPES[0]} {CARD_NUMBERS[ACE_INDEX]}'
            ),
            inline = True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_done_field(embed, user, guild, hand):
    """
    Tests whether ``add_done_field`` works as intended.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    user : ``ClientUserBase``
        The user who owns the hand.
    guild : ``None | Guild``
        The respective guild where the game is.
    hand : ``Hand``
        The hand to add its done field for.
    
    Returns
    -------
    output : ``Embed``
    """
    output = add_done_field(embed, user, guild, hand)
    vampytest.assert_instance(output, Embed)
    return output
