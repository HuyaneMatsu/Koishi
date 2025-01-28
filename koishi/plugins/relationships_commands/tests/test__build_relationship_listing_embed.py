from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Embed, GuildProfile, ICON_TYPE_STATIC, Icon, User

from ...relationships_core import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU, RELATIONSHIP_TYPE_MISTRESS,
    Relationship, RelationshipRequest
)
from ...user_balance import UserBalance

from ..embed_builders import build_relationship_listing_embed


def _iter_options():
    user_id_00 = 202501040040
    user_id_01 = 202501040041
    user_id_02 = 202501040042
    user_id_03 = 202501040043
    user_id_04 = 202501040044
    user_id_05 = 202501040045
    user_id_06 = 202501040046
    user_id_07 = 202501040047
    user_id_08 = 202501040048
    user_id_09 = 202501040049
    user_id_10 = 202501040050
    user_id_11 = 202501040051
    user_id_12 = 202501040052
    user_id_13 = 202501040053
    user_id_14 = 202501040054
    
    guild_id = 202501040100
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_00 = User.precreate(user_id_00, name = 'Satori', avatar = Icon(ICON_TYPE_STATIC, 100))
    user_00.guild_profiles[guild_id] = GuildProfile(nick = 'Sato', avatar = Icon(ICON_TYPE_STATIC, 101))
    
    user_01 = User.precreate(user_id_01, name = 'Koishi', avatar = Icon(ICON_TYPE_STATIC, 102))
    user_01.guild_profiles[guild_id] = GuildProfile(nick = 'Koi', avatar = Icon(ICON_TYPE_STATIC, 103))
    
    user_02 = User.precreate(user_id_02, name = 'Rin', avatar = Icon(ICON_TYPE_STATIC, 104))
    user_02.guild_profiles[guild_id] = GuildProfile(nick = 'Orin', avatar = Icon(ICON_TYPE_STATIC, 105))
    
    user_03 = User.precreate(user_id_03, name = 'Utsuho', avatar = Icon(ICON_TYPE_STATIC, 106))
    user_03.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu', avatar = Icon(ICON_TYPE_STATIC, 107))
    
    user_04 = User.precreate(user_id_04, name = 'Alice', avatar = Icon(ICON_TYPE_STATIC, 108))
    user_04.guild_profiles[guild_id] = GuildProfile(nick = 'Alicia', avatar = Icon(ICON_TYPE_STATIC, 109))
    
    user_05 = User.precreate(user_id_05, name = 'Flandre', avatar = Icon(ICON_TYPE_STATIC, 110))
    user_05.guild_profiles[guild_id] = GuildProfile(nick = 'Flan', avatar = Icon(ICON_TYPE_STATIC, 111))
    
    user_06 = User.precreate(user_id_06, name = 'Remilia', avatar = Icon(ICON_TYPE_STATIC, 112))
    user_06.guild_profiles[guild_id] = GuildProfile(nick = 'Remi', avatar = Icon(ICON_TYPE_STATIC, 113))
    
    user_07 = User.precreate(user_id_07, name = 'Suwako', avatar = Icon(ICON_TYPE_STATIC, 114))
    user_07.guild_profiles[guild_id] = GuildProfile(nick = 'brrrr', avatar = Icon(ICON_TYPE_STATIC, 115))
    
    user_08 = User.precreate(user_id_08, name = 'Kanako', avatar = Icon(ICON_TYPE_STATIC, 116))
    user_08.guild_profiles[guild_id] = GuildProfile(nick = 'Mountains of Faith', avatar = Icon(ICON_TYPE_STATIC, 117))
    
    user_09 = User.precreate(user_id_09, name = 'Shinki', avatar = Icon(ICON_TYPE_STATIC, 118))
    user_09.guild_profiles[guild_id] = GuildProfile(nick = 'Demon', avatar = Icon(ICON_TYPE_STATIC, 119))
    
    user_10 = User.precreate(user_id_10, name = 'Sariel', avatar = Icon(ICON_TYPE_STATIC, 120))
    user_10.guild_profiles[guild_id] = GuildProfile(nick = 'Angel', avatar = Icon(ICON_TYPE_STATIC, 121))
    
    user_11 = User.precreate(user_id_11, name = 'Mokou', avatar = Icon(ICON_TYPE_STATIC, 122))
    user_11.guild_profiles[guild_id] = GuildProfile(nick = 'Phoenix', avatar = Icon(ICON_TYPE_STATIC, 123))
    
    user_12 = User.precreate(user_id_12, name = 'Kaguya', avatar = Icon(ICON_TYPE_STATIC, 124))
    user_12.guild_profiles[guild_id] = GuildProfile(nick = 'Stare', avatar = Icon(ICON_TYPE_STATIC, 125))
    
    user_13 = User.precreate(user_id_13, name = 'Keine', avatar = Icon(ICON_TYPE_STATIC, 126))
    user_13.guild_profiles[guild_id] = GuildProfile(nick = 'Caver', avatar = Icon(ICON_TYPE_STATIC, 127))
    
    user_14 = User.precreate(user_id_14, name = 'Chen', avatar = Icon(ICON_TYPE_STATIC, 128))
    user_14.guild_profiles[guild_id] = GuildProfile(nick = 'Honk', avatar = Icon(ICON_TYPE_STATIC, 129))
    
    # self target
    
    user_balance_00 = UserBalance(user_id_01)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        None,
        None,
        None,
        None,
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
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
    user_balance_01 = UserBalance(user_id_01)
    user_balance_01.relationship_divorces = 4
    user_balance_01.relationship_slots = 9
    user_balance_01.relationship_value = 9999
    
    relationship_00 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_01 = Relationship(user_id_01, user_id_03, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_02 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_03 = Relationship(user_id_02, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    relationship_request_00 = RelationshipRequest(user_id_01, user_id_05, RELATIONSHIP_TYPE_SISTER_BIG, 1200)
    
    yield (
        user_00,
        user_01,
        user_balance_01,
        [
            relationship_00,
            relationship_01,
            relationship_02,
        ],
        [
            (relationship_00, [relationship_03]),
        ],
        [
            relationship_request_00,
        ],
        [
            user_02,
            user_03,
            user_04,
            user_05,
        ],
        guild_id,
        Embed(
            'Koi\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id_01}/avatars/00000000000000000000000000000067.png',
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
            'Orin',
        ).add_field(
            'Big sister',
            'Flan'
        ).add_field(
            'Lil sisters',
            (
                'Okuu\n'
                'Alicia (in law)'
            ),
        ).add_footer(
            'To propose to Koi you need at least 21717 hearts.',
            icon_url = f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id_00}/avatars/00000000000000000000000000000065.png'
        )
    )
    
    # reversed relationship & unset
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    relationship_01 = Relationship(user_id_00, user_id_02, RELATIONSHIP_TYPE_UNSET, 1200, now)
    relationship_02 = Relationship(user_id_00, user_id_03, RELATIONSHIP_TYPE_DAUGHTER, 1200, now)
    relationship_03 = Relationship(user_id_00, user_id_04, RELATIONSHIP_TYPE_MAID, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            relationship_00,
            relationship_01,
            relationship_02,
            relationship_03,
        ],
        None,
        None,
        [
            user_01,
            user_02,
            user_03,
            user_04,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '3172 - 6056\n'
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
            'Big sister',
            'Koishi',
        ).add_field(
            'Mama',
            'Utsuho',
        ).add_field(
            'Master',
            'Alice',
        ).add_field(
            'Unset',
            'Rin',
        ),
    )
    
    # Test bugfix: reversed waifu relation switched up extended relationships' users
    # So displayed wrong user in short.
    
    user_balance_01 = UserBalance(user_id_01)
    user_balance_01.relationship_divorces = 0
    user_balance_01.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_00, RELATIONSHIP_TYPE_MAMA, 1200, now)
    relationship_02 = Relationship(user_id_03, user_id_00, RELATIONSHIP_TYPE_SISTER_LIL, 1200, now)
    
    yield (
        user_00,
        user_01,
        user_balance_01,
        [
            relationship_00,
        ],
        [
            (relationship_00, [relationship_01, relationship_02]),
        ],
        None,
        [
            user_00,
            user_02,
            user_03,
        ],
        0,
        Embed(
            'Koishi\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_01}/00000000000000000000000000000066.png',
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Waifu',
            'Satori'
        ).add_field(
            'Lil sister',
            'Utsuho (in law)',
        ).add_field(
            'Mama',
            'Rin (in law)',
        ),
    )
    
    # sharing through waifu
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1200, now)
    relationship_02 = Relationship(user_id_01, user_id_03, RELATIONSHIP_TYPE_SISTER_BIG, 1200, now)
    relationship_03 = Relationship(user_id_04, user_id_01, RELATIONSHIP_TYPE_MAMA, 1200, now)
    relationship_04 = Relationship(user_id_01, user_id_05, RELATIONSHIP_TYPE_MAMA, 1200, now)
    relationship_05 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MISTRESS, 1200, now)
    
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # waifu
            relationship_00,
        ],
        [
            # waifus'
            (
                relationship_00,
                (
                    # big sister is your big sister (in law)
                    relationship_01,
                    # lil sister is your lil sister (in law)
                    relationship_02,
                    # mama is your mama (in law)
                    relationship_03,
                    # daughter is your daughter (in law)
                    relationship_04,
                    # maid is your maid (in law)
                    relationship_05,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
            user_03,
            user_04,
            user_05,
            user_06,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '2200 - 4200\n'
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Waifu',
            'Koishi',
        ).add_field(
            'Big sister',
            'Rin (in law)',
        ).add_field(
            'Lil sister',
            'Utsuho (in law)',
        ).add_field(
            'Mama',
            'Alice (in law)',
        ).add_field(
            'Daughter',
            'Flandre (in law)',
        ).add_field(
            'Maid',
            'Remilia (in law)',
        ),
    )
    
    # sharing through big sister
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # big sister
            relationship_00,
        ],
        [
            # big sister''s
            (
                relationship_00,
                (
                    # waifu is your big sister (in law)
                    relationship_01,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Big sisters',
            (
                'Koishi\n'
                'Rin (in law)'
            ),
        ),
    )
    
    # sharing through lil sister
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # lil sister
            relationship_00,
        ],
        [
            # lil sister''s
            (
                relationship_00,
                (
                    # waifu is your lil sister (in law)
                    relationship_01,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '2200 - 4200\n'
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Lil sisters',
            (
                'Koishi\n'
                'Rin (in law)'
            ),
        ),
    )
    
    # sharing through mama
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_MAMA, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # mama
            relationship_00,
        ],
        [
            # mama''s
            (
                relationship_00,
                (
                    # waifu is your mama (in law)
                    relationship_01,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Mamas',
            (
                'Koishi\n'
                'Rin (in law)'
            ),
        ),
    )
    
    # sharing through daughter
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_MAMA, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # daughter
            relationship_00,
        ],
        [
            # daughter''s
            (
                relationship_00,
                (
                    # waifu is your daughter (in law)
                    relationship_01,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '2200 - 4200\n'
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Daughters',
            (
                'Koishi\n'
                'Rin (in law)'
            ),
        ),
    )
    
    # sharing through mistress
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_MISTRESS, 2000, now)
    relationship_01 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1200, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # mistress
            relationship_00,
        ],
        [
            # mistress''s
            (
                relationship_00,
                (
                    # waifu is your mistress (in law)
                    relationship_01,
                ),
            ),
        ],
        None,
        [
            user_01,
            user_02,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Masters',
            (
                'Koishi\n'
                'Rin (in law)'
            ),
        ),
    )
    
    # sharing through maid
    user_balance_00 = UserBalance(user_id_00)
    user_balance_00.relationship_divorces = 0
    user_balance_00.relationship_slots = 1
    
    relationship_00 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 2000, now)
    
    yield (
        user_00,
        user_00,
        user_balance_00,
        [
            # maid
            relationship_00,
        ],
        None, # no sharing currently
        None,
        [
            user_01,
        ],
        0,
        Embed(
            'Satori\'s relationship info',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id_00}/00000000000000000000000000000064.png',
        ).add_field(
            'Value',
            (
                '```\n'
                '2200 - 4200\n'
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
                '1 / 1\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Maid',
            'Koishi',
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
