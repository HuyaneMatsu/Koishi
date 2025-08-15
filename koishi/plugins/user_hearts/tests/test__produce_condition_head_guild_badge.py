import vampytest
from hata import Guild, InteractionEvent, User

from ....bot_utils.daily import ConditionGuildBadge

from ..rendering import produce_condition_head_guild_badge


def _iter_options():
    guild_id = 202507120010
    guild = Guild.precreate(guild_id, name = 'Wonderhell')
    
    yield (
        ConditionGuildBadge(guild),
        InteractionEvent.precreate(
            202507120011,
            guild = guild,
            user = User.precreate(202507120012),
        ),
        f'**Has tag of {guild.name}:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_condition_head_guild_badge(condition, interaction_event):
    """
    Tests whether ``produce_condition_head_guild_badge`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionGuildBadge``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_condition_head_guild_badge(condition, interaction_event))
