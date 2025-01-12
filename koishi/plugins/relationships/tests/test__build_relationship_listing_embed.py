from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Embed, GuildProfile, ICON_TYPE_STATIC, Icon, User

from ...user_balance import UserBalance

from ..embed_builders import build_relationship_listing_embed
from ..relationship import Relationship
from ..relationship_request import RelationshipRequest
from ..relationship_types import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL,
    RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU
)


def _iter_options():
    user_id_0 = 202501040040
    user_id_1 = 202501040041
    user_id_2 = 202501040042
    user_id_3 = 202501040043
    user_id_4 = 202501040044
    user_id_5 = 202501040045
    user_id_6 = 202501040046
    
    guild_id = 202501040047
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_0 = User.precreate(user_id_0, name = 'Satori', avatar = Icon(ICON_TYPE_STATIC, 100))
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato', avatar = Icon(ICON_TYPE_STATIC, 101))
    
    user_1 = User.precreate(user_id_1, name = 'Koishi', avatar = Icon(ICON_TYPE_STATIC, 102))
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Koi', avatar = Icon(ICON_TYPE_STATIC, 103))
    
    user_2 = User.precreate(user_id_2, name = 'Rin', avatar = Icon(ICON_TYPE_STATIC, 104))
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Orin', avatar = Icon(ICON_TYPE_STATIC, 105))
    
    user_3 = User.precreate(user_id_3, name = 'Utsuho', avatar = Icon(ICON_TYPE_STATIC, 106))
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu', avatar = Icon(ICON_TYPE_STATIC, 107))
    
    user_4 = User.precreate(user_id_4, name = 'Alice', avatar = Icon(ICON_TYPE_STATIC, 108))
    user_4.guild_profiles[guild_id] = GuildProfile(nick = 'Alicia', avatar = Icon(ICON_TYPE_STATIC, 109))
    
    user_5 = User.precreate(user_id_5, name = 'Flandre', avatar = Icon(ICON_TYPE_STATIC, 110))
    user_5.guild_profiles[guild_id] = GuildProfile(nick = 'Flan', avatar = Icon(ICON_TYPE_STATIC, 111))
    
    user_6 = User.precreate(user_id_6, name = 'Remilia', avatar = Icon(ICON_TYPE_STATIC, 112))
    user_6.guild_profiles[guild_id] = GuildProfile(nick = 'Remi', avatar = Icon(ICON_TYPE_STATIC, 113))
    
    user_balance_0 = UserBalance(user_id_0)
    user_balance_0.relationship_divorces = 0
    user_balance_0.relationship_slots = 1
    
    user_balance_1 = UserBalance(user_id_1)
    user_balance_1.relationship_divorces = 4
    user_balance_1.relationship_slots = 9
    user_balance_1.relationship_value = 9999
    
    relationship_0 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_1 = Relationship(user_id_1, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_6, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_3 = Relationship(user_id_2, user_id_4, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    relationship_4 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    relationship_5 = Relationship(user_id_1, user_id_3, RELATIONSHIP_TYPE_UNSET, 1200, now)
    relationship_6 = Relationship(user_id_1, user_id_4, RELATIONSHIP_TYPE_DAUGHTER, 1200, now)
    relationship_7 = Relationship(user_id_1, user_id_5, RELATIONSHIP_TYPE_MAID, 1200, now)
    
    relationship_request_0 = RelationshipRequest(user_id_1, user_id_5, RELATIONSHIP_TYPE_SISTER_BIG, 1200)
    
    # self target
    yield (
        user_0,
        user_0,
        user_balance_0,
        None,
        None,
        None,
        None,
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_0}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '550 - 1050\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Divorces',
            (
                '```\n'
                '0\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Slots',
            (
                '```\n'
                '0 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Relationships',
            '*none*',
        )
    )
    
    # other target + value + relationships + indirect relationships + relationship requests+ nicks
    yield (
        user_0,
        user_1,
        user_balance_1,
        [
            relationship_0,
            relationship_1,
            relationship_2,
        ],
        [
            (relationship_0, [relationship_3]),
        ],
        [
            relationship_request_0,
        ],
        [
            user_2,
            user_3,
            user_4,
            user_6,
        ],
        guild_id,
        Embed(
            'Koi\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id_1}/avatars/00000000000000000000000000000067.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '11430 - 21821\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Divorces',
            (
                '```\n'
                '4\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Slots',
            (
                '```\n'
                '4 (3 + 1) / 9\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Waifu',
            (
                'Orin'
            ),
        ).add_field(
            'Big sister(s)',
            (
                'Remi'
            ),
        ).add_field(
            'Lil sister(s)',
            (
                'Okuu\n'
                'Alicia (in law)'
            ),
        ).add_footer(
            'To propose to Koi you need at least 21717 hearts.',
            icon_url = f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id_0}/avatars/00000000000000000000000000000065.png'
        )
    )
    
    
    # reversed relationship & unset
    yield (
        user_0,
        user_0,
        user_balance_0,
        [
            relationship_4,
            relationship_5,
            relationship_6,
            relationship_7,
        ],
        None,
        None,
        [
            user_2,
            user_3,
            user_4,
            user_5,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_0}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '550 - 1050\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Divorces',
            (
                '```\n'
                '0\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Slots',
            (
                '```\n'
                '4 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Big sister(s)',
            (
                'Rin'
            ),
        ).add_field(
            'Mama',
            (
                'Alice'
            ),
        ).add_field(
            'Master',
            (
                'Flandre'
            ),
        ).add_field(
            'Unset',
            (
                'Utsuho'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_relationship_listing_embed(
    source_user,
    target_user,
    target_user_balance,
    target_relationship_listing,
    target_relationship_listing_extend,
    target_relationship_request_listing,
    users,
    guild_id,
):
    """
    tests whether ``build_relationship_listing_embed`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is listing the relationships.
    
    target_user : ``ClientUserBase``
        The user who's relationships are being listed.
    
    target_user_balance : ``UserBalance``
        The targeted user's user balance.
    
    target_relationship_listing : `None | list<Relationship>`
        The targeted user's relationships.
    
    target_relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        Indirect relationships of the targeted user.
    
    target_relationship_request_listing : `None | list<RelationshipProposal>`
        The outgoing relationship proposals of the targeted user.
    
    users : `None | list<ClientUserBase>`
        The user entities the `target_user` has relationships with.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_relationship_listing_embed(
        source_user,
        target_user,
        target_user_balance,
        target_relationship_listing,
        target_relationship_listing_extend,
        target_relationship_request_listing,
        users,
        guild_id,
    )
    vampytest.assert_instance(output, Embed)
    return output
