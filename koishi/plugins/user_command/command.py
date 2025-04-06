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
    from ..stats_core import get_stats
except ImportError:
    if not MARISA_MODE:
        raise
    
    USER_STATS_AVAILABLE = False
    USER_EQUIPMENT_AVAILABLE = False
    USER_EQUIP_AVAILABLE = False
    USER_INVENTORY_AVAILABLE = False
    USER_DISCARD_ITEM_AVAILABLE = False
else:
    try:
        from ..user_stats import build_stats_embed
    except ImportError:
        if not MARISA_MODE:
            raise
        
        USER_STATS_AVAILABLE = False
    
    else:
        USER_STATS_AVAILABLE = True
    
    try:
        from ..user_equpment import build_equipment_embed
    except ImportError:
        if not MARISA_MODE:
            raise
        
        USER_EQUIPMENT_AVAILABLE = False
    
    else:
        USER_EQUIPMENT_AVAILABLE = True

    try:
        from ..user_equip import (
            ITEM_SLOTS, build_failure_embed_empty_equipment_slot, build_failure_embed_no_equipment_like,
            build_failure_embed_same_item, build_success_embed_item_equipped, build_success_embed_item_unequipped,
            build_success_embed_item_replaced, equip_item, get_equip_item_suggestions, unequip_item
        )
    except ImportError:
        if not MARISA_MODE:
            raise
        
        USER_EQUIP_AVAILABLE = False
    
    else:
        USER_EQUIP_AVAILABLE = True
    
    try:
        from ..user_inventory import (
            SORT_BY_DEFAULT, SORT_BYES, SORT_ORDER_DEFAULT, SORT_ORDERS, get_inventory_page_response
        )
    except ImportError:
        if not MARISA_MODE:
            raise
        
        USER_INVENTORY_AVAILABLE = False
    
    else:
        USER_INVENTORY_AVAILABLE = True
    
    try:
        from ..user_discard_item import (
            build_failure_embed_no_item_discarded, build_failure_embed_no_item_like, build_success_embed_item_discarded,
            discard_item, get_discard_item_suggestions
        )
    except ImportError:
        if not MARISA_MODE:
            raise
        
        USER_DISCARD_ITEM_AVAILABLE = False
    
    else:
        USER_DISCARD_ITEM_AVAILABLE = True


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
    @USER_COMMANDS.interactions(name = 'stats')
    async def user_stats_command(
        event,
        user: ('user', 'Select someone else?') = None,
    ):
        """
        Shows your stats.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        user : `None`, ``ClientUserBase`` = `None`, Optional
            The selected user.
        
        Returns
        -------
        response : ``Embed``
        """
        if user is None:
            user = event.user
        
        stats = await get_stats(user.id)
        return build_stats_embed(user, stats, event.guild_id)


if USER_EQUIPMENT_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'equipment')
    async def user_equipment_command(
        event,
        user: (ClientUserBase, 'Select someone else?') = None,
    ):
        """
        Shows your equipment.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        user : `None`, ``ClientUserBase`` = `None`, Optional
            The selected user.
        
        Returns
        -------
        response : ``Embed``
        """
        if user is None:
            user = event.user
        
        stats = await get_stats(user.id)
        return build_equipment_embed(user, stats, event.guild_id)


if USER_EQUIP_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'equip')
    async def user_equip_command(
        event,
        item_slot : (ITEM_SLOTS, 'Select an item slot'),
        item_name : (str, 'The item\'s name', 'item'),
    ):
        """
        Equips the selected item at the selected item slot.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        item_slot : `int`
            The selected user.
        
        item_name : `str`
            The give item name.
        
        Returns
        -------
        response : ``Embed``
        """
        old_item, new_item = await equip_item(event.user_id, item_slot, item_name)
        if new_item is None:
            return build_failure_embed_no_equipment_like(item_slot, item_name)
        
        if old_item is new_item:
            return build_failure_embed_same_item(item_slot, old_item)
        
        if old_item is None:
            return build_success_embed_item_equipped(item_slot, new_item)
        
        return build_success_embed_item_replaced(item_slot, old_item, new_item)
    
    
    @user_equip_command.autocomplete('item')
    async def autocomplete_item(event, value):
        """
        Autocompletes the item to equip. Item type must be selected already.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        value : `None | str`
            The typed in value.
        
        Returns
        -------
        suggestions : `None | list<(str, int)>`
        """
        item_slot = event.interaction.get_value_of('equip', 'item-slot')
        if item_slot is None:
            return
        
        try:
            item_slot = int(item_slot)
        except ValueError:
            return
        
        return await get_equip_item_suggestions(event.user_id, item_slot, value)
    
    
    @USER_COMMANDS.interactions(name = 'unequip')
    async def user_unequip_command(
        event,
        item_slot : (ITEM_SLOTS, 'Select an item slot'),
    ):
        """
        Unequips the item from the selected item slot.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        item_slot : `int`
            The selected user.
        
        Returns
        -------
        response : ``Embed``
        """
        old_item = await unequip_item(event.user_id, item_slot)
        if old_item is None:
            return build_failure_embed_empty_equipment_slot(item_slot)
        
        return build_success_embed_item_unequipped(item_slot, old_item)


if USER_INVENTORY_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'inventory')
    async def user_inventory_command(
        event,
        sort_by : (SORT_BYES, 'How to sort the items.') = SORT_BY_DEFAULT,
        sort_order : (SORT_ORDERS, 'Sort ordering') = SORT_ORDER_DEFAULT,
    ):
        """
        Displays your inventory.
        
        This function is a coroutine generator.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        sort_by : `int` = `SORT_BY_DEFAULT`, Optional
            How to sort the items.
        
        sort_order : `int` = `SORT_ORDER_DEFAULT`, Optional
            Sort ordering.
        
        Returns
        -------
        response : ``InteractionResponse``
        """
        yield
        yield await get_inventory_page_response(event.user_id, sort_by, sort_order, 0)


if USER_DISCARD_ITEM_AVAILABLE:
    @USER_COMMANDS.interactions(name = 'discard-item')
    async def user_discard_command(
        event,
        item_name : (str, 'The item\'s name', 'item'),
        amount : ('expression', 'The amount of items to discard.'),
    ):
        """
        Discard items from your inventory.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        item_slot : `int`
            The selected user.
        
        item_name : `str`
            The give item name.
        
        Returns
        -------
        response : ``Embed``
        """
        item, discarded_amount, new_amount = await discard_item(event.user_id, item_name, amount)
        if item is None:
            return build_failure_embed_no_item_like(item_name)
        
        if not discarded_amount:
            return build_failure_embed_no_item_discarded(item, new_amount)
        
        return build_success_embed_item_discarded(item, discarded_amount, new_amount)
    
    
    @user_discard_command.autocomplete('item')
    async def autocomplete_item(event, value):
        """
        Autocompletes the item to discard.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        
        value : `None | str`
            The typed in value.
        
        Returns
        -------
        suggestions : `None | list<(str, int)>`
        """
        return await get_discard_item_suggestions(event.user_id, value)
