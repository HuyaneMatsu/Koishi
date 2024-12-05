import vampytest
from hata import Guild, InteractionEvent, Role, User

from ....bot_utils.daily import ConditionRole

from ..rendering import render_condition_head_role_into


def _iter_options():
    role_id = 202412020002
    guild_id = 202412020003
    role = Role.precreate(role_id, guild_id = guild_id, name = 'pudding')
    
    yield (
        ConditionRole(role),
        InteractionEvent.precreate(
            202412020004,
            guild = Guild.precreate(guild_id),
            user = User.precreate(202412020005),
        ),
        f'**Has role {role.mention}:**\n',
    )
    
    yield (
        ConditionRole(Role.precreate(role_id, guild_id = guild_id)),
        InteractionEvent.precreate(
            202412020006,
            user = User.precreate(202412020007),
        ),
        f'**Has role @\u200b{role.name}:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_condition_head_role_into(condition, interaction_event):
    """
    Tests whether ``render_condition_head_role_into`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionRole``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    into = render_condition_head_role_into([], condition, interaction_event)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
