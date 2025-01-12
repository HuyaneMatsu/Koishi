import vampytest
from hata import CDN_ENDPOINT, Embed, Guild, GuildProfile, Icon, IconType, InteractionEvent, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import (
    EMOJI_COUNT_DAILY_BY_WAIFU, EMOJI_COUNT_DAILY_FOR_WAIFU, EMOJI_COUNT_DAILY_SELF, EMOJI_COUNT_TOP_GG_VOTE,
    EMOJI_DAILY_STREAK
)
from ..embed_building import build_stats_embed


def _iter_options():
    guild_id = 202412030051
    user_id = 202412030050
    user = User.precreate(user_id, name = 'koishi')
    guild = Guild.precreate(guild_id, users = [user])
    user.guild_profiles[guild_id] = GuildProfile(nick = 'satori', avatar = Icon(IconType.animated, 2))
    
    yield (
        InteractionEvent.precreate(
            202412030052,
            user = user,
            guild = guild,
        ),
        user,
        20,
        12,
        1,
        2,
        3,
        4,
        Embed(
            color = COLOR__GAMBLING,
        ).add_author(
            'Heart stats for satori',
            f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000002.gif',
        ).add_field(
            f'{EMOJI__HEART_CURRENCY} Hearts',
            '```\n20\n```',
            inline = True,
        ).add_field(
            f'{EMOJI_DAILY_STREAK} Streak',
            '```\n12\n```',
            inline = True,
        ).add_field(
            f'{EMOJI_COUNT_DAILY_SELF} Claimed dailies',
            '```\n1\n```',
            inline = True,
        ).add_field(
            f'{EMOJI_COUNT_DAILY_FOR_WAIFU} Claimed for related',
            '```\n3\n```',
            inline = True,
        ).add_field(
            f'{EMOJI_COUNT_DAILY_BY_WAIFU} Claimed by related',
            '```\n2\n```',
            inline = True,
        ).add_field(
            f'{EMOJI_COUNT_TOP_GG_VOTE} Top.gg votes',
            '```\n4\n```',
            inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_stats_embed(
    interaction_event,
    target_user,
    balance,
    streak,
    count_daily_self,
    count_daily_by_related,
    count_daily_for_related,
    count_top_gg_vote,
):
    """
    Tests whether ``build_stats_embed`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    count_daily_self : `int`
        The amount the user claimed their own daily.
    
    count_daily_by_related : `int`
        The amount the user's daily has been claimed.
    
    count_daily_for_related : `int`
        The amount the user claimed other's daily.
    
    count_top_gg_vote : `int`
        The amount the user voted on top.gg.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_stats_embed(
        interaction_event,
        target_user,
        balance,
        streak,
        count_daily_self,
        count_daily_by_related,
        count_daily_for_related,
        count_top_gg_vote,
    )
    vampytest.assert_instance(output, Embed)
    return output
