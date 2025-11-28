__all__ = ()

from config import MARISA_MODE

from ...bots import FEATURE_CLIENTS

try:
    from ..guild_icon import ICON_KIND_ICON, ICON_KINDS, build_icon_interaction_response 
except ImportError:
    if not MARISA_MODE:
        raise
    
    GUILD_ICON_AVAILABLE = False
else:
    GUILD_ICON_AVAILABLE = True


try:
    from ..guild_info import command_guild_info
except ImportError:
    if not MARISA_MODE:
        raise
    
    GUILD_INFO_AVAILABLE = False
else:
    GUILD_INFO_AVAILABLE = True


try:
    from ..quest_board import command_guild_quest_board
except ImportError:
    if not MARISA_MODE:
        raise
    
    GUILD_QUEST_BOARD_AVAILABLE = False
else:
    GUILD_QUEST_BOARD_AVAILABLE = True


GUILD_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'guild',
    description = 'guild utility commands',
    is_global = True,
    integration_context_types = ['guild'],
)


if GUILD_INFO_AVAILABLE:
    GUILD_COMMANDS.interactions(command_guild_info, name = 'info')


if GUILD_ICON_AVAILABLE:
    @GUILD_COMMANDS.interactions(name = 'icon')
    async def guild_icon_slash_command(
        event,
        icon_kind: (ICON_KINDS, 'Which icon of the guild?', 'icon') = ICON_KIND_ICON,
    ):
        """
        Shows the guild's icon.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received event.
        
        field : `str` = `ICON_KIND_ICON`, Optional
            The icon's name to show.
        
        Returns
        -------
        response : ``InteractionResponse``
        """
        guild = event.guild
        if (guild is None):
            return
        
        return build_icon_interaction_response(guild, icon_kind)


if GUILD_QUEST_BOARD_AVAILABLE:
    GUILD_COMMANDS.interactions(command_guild_quest_board, name = 'quest-board')
