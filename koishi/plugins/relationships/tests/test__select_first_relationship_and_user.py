from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ClientUserBase, GuildProfile, User

from ..relationship import Relationship
from ..relationship_completion import _select_first_relationship_and_user
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG


def _iter_options():
    user_id_0 = 202501070000
    user_id_1 = 202501080002
    user_id_2 = 202501070012
    user_id_3 = 202501070013
    
    guild_id = 202501070014
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    user_1 = User.precreate(user_id_1, name = 'Rin')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Orin')
    
    user_2 = User.precreate(user_id_2, name = 'Utsuho')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_2, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        [user_0, user_1, user_2],
        'Sa',
        0,
        (relationship_0, user_0),
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        [user_0, user_1, user_2],
        'Ok',
        0,
        None,
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        [user_0, user_1, user_2],
        'Ok',
        guild_id,
        (relationship_2, user_2),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_first_relationship_and_user(relationships, users, value, guild_id):
    """
    Tests whether ``_select_first_relationship_and_user`` works as intended.
    
    Parameters
    ----------
    relationships : `list<Relationship>`
        Relationships to filter from.
    
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
    output = _select_first_relationship_and_user(relationships, users, value, guild_id)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        vampytest.assert_eq(len(output), 2)
        vampytest.assert_instance(output[0], Relationship)
        vampytest.assert_instance(output[1], ClientUserBase)
    
    return output
