from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ClientUserBase, GuildProfile, User

from ..relationship import Relationship
from ..relationship_completion import _select_first_extender_relationship_and_relationship_and_user
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202501090030
    user_id_1 = 202501080002
    user_id_2 = 202501070012
    user_id_3 = 202501070013
    user_id_4 = 202501090024
    user_id_5 = 202501090025
    user_id_6 = 202501090026
    
    guild_id = 202501070014
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    user_1 = User.precreate(user_id_1, name = 'Rin')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Orin')
    
    user_2 = User.precreate(user_id_2, name = 'Utsuho')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu')
    
    user_3 = User.precreate(user_id_3, name = 'Koishi')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user_4 = User.precreate(user_id_4, name = 'Flandre')
    user_4.guild_profiles[guild_id] = GuildProfile(nick = 'Pudding')
    
    user_5 = User.precreate(user_id_5, name = 'Remilia')
    user_5.guild_profiles[guild_id] = GuildProfile(nick = 'Bat')
    
    user_6 = User.precreate(user_id_6, name = 'Sakuya')
    user_6.guild_profiles[guild_id] = GuildProfile(nick = 'Suyu')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_2, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_3 = Relationship(user_id_0, user_id_4, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_4 = Relationship(user_id_4, user_id_0, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_5 = Relationship(user_id_5, user_id_4, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_6 = Relationship(user_id_4, user_id_6, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        None,
        [user_0, user_1, user_2],
        'Sa',
        0,
        (None, relationship_0, user_0),
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        None,
        [user_0, user_1, user_2],
        'Ok',
        0,
        None,
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        None,
        [user_0, user_1, user_2],
        'Ok',
        guild_id,
        (None, relationship_2, user_2),
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [
            (relationship_3, [relationship_5, relationship_6]),
        ],
        [user_0, user_1, user_2, user_3, user_4, user_5, user_6],
        'Saku',
        0,
        (relationship_3, relationship_6, user_6),
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [
            (relationship_3, [relationship_5, relationship_6]),
        ],
        [user_0, user_1, user_2, user_3, user_4, user_5, user_6],
        'Suyu',
        0,
        None,
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2, relationship_4],
        [
            (relationship_4, [relationship_5, relationship_6]),
        ],
        [user_0, user_1, user_2, user_3, user_4, user_5, user_6],
        'Suyu',
        guild_id,
        (relationship_4, relationship_6, user_6),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_first_extender_relationship_and_relationship_and_user(
    relationship_listing, relationship_listing_extend, users, value, guild_id
):
    """
    Tests whether ``_select_first_extender_relationship_and_relationship_and_user`` works as intended.
    
    Parameters
    ----------
    relationship_listing : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    users : `list<ClientUserBase>`
        The users to filter from.
    
    value : `None | str`
        Value to filter for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | (Relationship, ClientUserBase)`
    """
    output = _select_first_extender_relationship_and_relationship_and_user(
        relationship_listing, relationship_listing_extend, users, value, guild_id
    )
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        vampytest.assert_eq(len(output), 3)
        vampytest.assert_instance(output[0], Relationship, nullable = True)
        vampytest.assert_instance(output[1], Relationship)
        vampytest.assert_instance(output[2], ClientUserBase)
    
    return output
