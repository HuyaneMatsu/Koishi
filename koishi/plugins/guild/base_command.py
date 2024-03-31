__all__ = ()

from ...bots import FEATURE_CLIENTS


GUILD_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'guild',
    description = 'guild utility commands',
    is_global = True,
    integration_context_types = ['guild'],
)
