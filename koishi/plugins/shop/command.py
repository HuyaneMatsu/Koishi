__all__ = ()

from config import MARISA_MODE

from ...bots import FEATURE_CLIENTS


try:
    from ..relationship_divorces_command import command_burn_divorce_papers
except ImportError:
    if not MARISA_MODE:
        raise
    
    BURN_DIVORCE_PAPERS_COMMAND_AVAILABLE = False

else:
    BURN_DIVORCE_PAPERS_COMMAND_AVAILABLE = True


try:
    from ..relationship_slots_command import command_buy_relationship_slot
except ImportError:
    if not MARISA_MODE:
        raise
    
    BUY_RELATIONSHIP_SLOTS_COMMAND_AVAILABLE = False

else:
    BUY_RELATIONSHIP_SLOTS_COMMAND_AVAILABLE = True


try:
    from ..role_purchase import command_buy_role
except KeyError:
    if not MARISA_MODE:
        raise
    
    BUY_ROLE_COMMAND_AVAILABLE = False

else:
    BUY_ROLE_COMMAND_AVAILABLE = True


try:
    from ..user_stats_upgrade import command_upgrade_stats
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_STATS_UPDATE_AVAILABLE = False

else:
    USER_STATS_UPDATE_AVAILABLE = True


SHOP = FEATURE_CLIENTS.interactions(
    None,
    name = 'shop',
    description = 'Trade your hearts!',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

if BUY_RELATIONSHIP_SLOTS_COMMAND_AVAILABLE:
    SHOP.interactions(command_buy_relationship_slot, name = 'buy-relationship-slot')


if BURN_DIVORCE_PAPERS_COMMAND_AVAILABLE:
    SHOP.interactions(command_burn_divorce_papers, name = 'burn-divorce-papers')


if BUY_ROLE_COMMAND_AVAILABLE:
    SHOP.interactions(command_buy_role, name = 'roles')


if USER_STATS_UPDATE_AVAILABLE:
    SHOP.interactions(command_upgrade_stats, name = 'upgrade-stats')
