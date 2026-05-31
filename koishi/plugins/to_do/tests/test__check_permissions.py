import vampytest

from hata import GuildProfile, InteractionEvent, User

from ....bot_utils.constants import ROLE__SUPPORT__TESTER

from ..helpers import check_for_required_role


def test__check_for_required_role__no_role():
    """
    Tests whether ``check_for_required_role`` works as intended.
    
    Case: no role.
    """
    user = User.precreate(202409180011)
    interaction_event = InteractionEvent.precreate(202409180012, user = user)
    
    output = check_for_required_role(interaction_event)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_is_not(output, None)


def test__check_for_required_role__has_role():
    """
    Tests whether ``check_for_required_role`` works as intended.
    
    Case: has role.
    """
    user = User.precreate(202409180013)
    user.guild_profiles[ROLE__SUPPORT__TESTER.guild_id] = GuildProfile(
        role_ids = [ROLE__SUPPORT__TESTER.id], 
    )
    
    event = InteractionEvent.precreate(202409180014, user = user)
    
    output = check_for_required_role(event)
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_is(output, None)
