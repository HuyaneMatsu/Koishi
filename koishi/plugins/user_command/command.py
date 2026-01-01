__all__ = ()

from hata import ClientUserBase, Embed
from hata.ext.slash import InteractionResponse, abort

from ...bots import FEATURE_CLIENTS

from config import MARISA_MODE

try:
    from ..user_info import (
        ICON_KIND_AVATAR, ICON_KIND_BANNER, ICON_SOURCE_CHOICES_AVATAR, ICON_SOURCE_CHOICES_BANNER, ICON_SOURCE_LOCAL,
        build_user_icon_embed, build_user_info_components, build_user_info_embed
    )
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_INFO_AVAILABLE = False
else:
    USER_INFO_AVAILABLE = True


try:
    from ..user_hearts import (
        HEARTS_FIELD_CHOICES, HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER, HEARTS_FIELD_NAME_SHORT
    )
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_HEARTS_AVAILABLE = False

else:
    USER_HEARTS_AVAILABLE = True


try:
    from ..user_stats import command_user_stats
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_STATS_AVAILABLE = False

else:
    USER_STATS_AVAILABLE = True

try:
    from ..user_equipment import command_user_equipment
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_EQUIPMENT_AVAILABLE = False

else:
    USER_EQUIPMENT_AVAILABLE = True

try:
    from ..user_equip import command_user_equip, command_user_unequip
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_EQUIP_AVAILABLE = False

else:
    USER_EQUIP_AVAILABLE = True

try:
    from ..user_inventory import command_user_inventory
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_INVENTORY_AVAILABLE = False

else:
    USER_INVENTORY_AVAILABLE = True

try:
    from ..user_discard_item import command_user_discard_item
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_DISCARD_ITEM_AVAILABLE = False

else:
    USER_DISCARD_ITEM_AVAILABLE = True


try:
    from ..quest_board import command_user_quests
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_QUESTS_AVAILABLE = False

else:
    USER_QUESTS_AVAILABLE = True


try:
    from ..user_allocations import command_user_allocations
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_ALLOCATIONS_AVAILABLE = False

else:
    USER_ALLOCATIONS_AVAILABLE = True


try:
    from ..user_inspect_item import command_user_inspect_item
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_INSPECT_ITEM_AVAILABLE = False

else:
    USER_INSPECT_ITEM_AVAILABLE = True



USER_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'user',
    description = 'User commands',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)


if USER_INFO_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'avatar')
    async def user_avatar_command(
        event,
        user : (ClientUserBase, 'Choose a user!') = None,
        icon_source : (ICON_SOURCE_CHOICES_AVATAR, 'Which avatar of the user?', 'type') = ICON_SOURCE_LOCAL,
    ):
        """
        Shows your or the chosen user's avatar.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        user : `None | ClientUserBase` = `None`, Optional
            The user to get its avatar of.
        
        icon_source : `int` = `ICON_SOURCE_LOCAL`, Optional
            Icon source to show.
        
        Returns
        -------
        response : ``Embed``
        """
        if user is None:
            user = event.user
        
        return build_user_icon_embed(user, event.guild_id, ICON_KIND_AVATAR, icon_source)
    
    
    @USER_COMMANDS.interactions(name = 'banner')
    async def user_banner_command(
        client,
        event,
        user : (ClientUserBase, 'Choose a user!') = None,
        icon_source : (ICON_SOURCE_CHOICES_BANNER, 'Which banner of the user?', 'type') = ICON_SOURCE_LOCAL,
    ):
        """
        Shows your or the chosen user's banner.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        
        event : ``InteractionEvent``
            The received interaction event.
        
        user : `None | ClientUserBase` = `None`, Optional
            The user to get its banner of.
        
        icon_source : `int` = `ICON_SOURCE_LOCAL`, Optional
            Icon source to show.
        
        Yields
        -------
        response : `None | Embed
        """
        if user is None:
            user = event.user
        
        yield
        
        await client.user_get(user, force_update = True)
        
        yield build_user_icon_embed(user, event.guild_id, ICON_KIND_BANNER, icon_source)
    
    
    @USER_COMMANDS.interactions(name = 'info')
    async def user_info_command(
        event,
        user: (ClientUserBase, 'Check out someone other user?') = None,
    ):
        """
        Shows some information about your or about the selected user.
        
        This function is a coroutine.
        
        Parameters
        ----------
        user : `None | ClientUserBase` = `None`, Optional
            They targeted user.
        
        Returns
        -------
        response : ``InteractionResponse``
        """
        if user is None:
            user = event.user
        
        return InteractionResponse(
            components = build_user_info_components(user, event.guild_id),
            embed = build_user_info_embed(user, event.guild_id),
        )


if USER_HEARTS_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'hearts')
    async def user_hearts_command(
        interaction_event,
        target_user: (ClientUserBase, 'Do you wanna know some1 else\'s hearts?') = None,
        field: (HEARTS_FIELD_CHOICES, 'Choose a field!') = HEARTS_FIELD_NAME_SHORT,
    ):
        """
        How many hearts do you have?
        
        This function is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        
        target_user : `None | ClientUserBase`
            The targeted user.
        
        field : `str`
            The field to show.
        
        Returns
        -------
        response : ``InteractionResponse``
        """
        if target_user is None:
            target_user = interaction_event.user
        
        try:
            response_builder = HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER[field]
        except KeyError:
            return abort(f'Unknown field: {field!r}.')
        
        return await response_builder(interaction_event, target_user)


if USER_STATS_AVAILABLE:
    USER_COMMANDS.interactions(command_user_stats, name = 'stats')


if USER_EQUIPMENT_AVAILABLE:
    USER_COMMANDS.interactions(command_user_equipment, name = 'equipment')


if USER_EQUIP_AVAILABLE:
    USER_COMMANDS.interactions(command_user_equip, name = 'equip')
    USER_COMMANDS.interactions(command_user_unequip, name = 'unequip')


if USER_INVENTORY_AVAILABLE:
    USER_COMMANDS.interactions(command_user_inventory, name = 'inventory')


if USER_DISCARD_ITEM_AVAILABLE:
    USER_COMMANDS.interactions(command_user_discard_item, name = 'discard-item')


if USER_QUESTS_AVAILABLE:
    USER_COMMANDS.interactions(command_user_quests, name = 'quests')


if USER_ALLOCATIONS_AVAILABLE:
    USER_COMMANDS.interactions(command_user_allocations, name = 'allocations')


if USER_INSPECT_ITEM_AVAILABLE:
    USER_COMMANDS.interactions(command_user_inspect_item, name = 'inspect-item')
