import vampytest
from hata import Guild, GuildProfile, Permission, Role, User
from hata.ext.slash import InteractionAbortedError, InteractionResponse

from ..shared_constants import WORD_CONFIG__MUTE
from ..shared_helpers import check_user_cannot_be_admin


def test__check_user_cannot_be_admin__admin():
    """
    Tests whether ``check_user_cannot_be_admin`` works as intended.
    
    Case: The user is admin.
    """
    user_id = 202310180001
    role_id = 202310180002
    guild_id = 202310180003
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    role = Role.precreate(role_id, permissions = Permission(8))
    guild = Guild.precreate(guild_id, users = [user], roles = [role])
    
    with vampytest.assert_raises(
        InteractionAbortedError(
            InteractionResponse(
                f'Cannot {WORD_CONFIG__MUTE.name} admins.',
                abort = True,
                show_for_invoking_user_only = True,
            ),
        )
    ):
        check_user_cannot_be_admin(guild, user, WORD_CONFIG__MUTE)


def test__check_user_cannot_be_admin__pleb():
    """
    Tests whether ``check_user_cannot_be_admin`` works as intended.
    
    Case: The user is a pleb.
    """
    user_id = 202310180004
    guild_id = 202310180005
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    guild = Guild.precreate(guild_id, users = [user])
    
    check_user_cannot_be_admin(guild, user, WORD_CONFIG__MUTE)
