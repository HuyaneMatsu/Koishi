import vampytest

from hata import GuildProfile, InteractionEvent, User
from hata.ext.slash import InteractionAbortedError

from ....bot_utils.constants import ROLE__SUPPORT__TESTER

from ..helpers import check_permission


def test__check_permission__no_role():
    """
    Tests whether ``check_permission`` works as intended.
    
    Case: no role.
    """
    user = User.precreate(202409180011)
    event = InteractionEvent.precreate(202409180012, user = user)
    
    with vampytest.assert_raises(InteractionAbortedError):
        check_permission(event)


def test__check_permission__has_role():
    """
    Tests whether ``check_permission`` works as intended.
    
    Case: has role.
    """
    user = User.precreate(202409180013)
    user.guild_profiles[ROLE__SUPPORT__TESTER.guild_id] = GuildProfile(
        role_ids = [ROLE__SUPPORT__TESTER.id], 
    )
    
    event = InteractionEvent.precreate(202409180014, user = user)
    
    check_permission(event)
