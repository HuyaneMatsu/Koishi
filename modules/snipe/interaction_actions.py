__all__ = ()

from hata import Client
from hata.ext.slash import Row

from bots import SLASH_CLIENT

from .choice_type import ChoiceTypeEmoji, ChoiceTypeSoundboardSound, ChoiceTypeSticker
from .component_translate_tables import ACTIONS_DISABLE
from .constants import (
    CUSTOM_ID_SNIPE_ACTIONS_EMOJI, CUSTOM_ID_SNIPE_ACTIONS_SOUNDBOARD_SOUND, CUSTOM_ID_SNIPE_ACTIONS_STICKER
)
from .helpers import check_has_manage_guild_expressions_permission, translate_components


async def respond_with_actions(client, event, choice_type):
    """
    Edits the message's components adding the given row.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    choice_type : `type<ChoiceTypeBase>`
        Choice type.
    """
    if not await check_has_manage_guild_expressions_permission(client, event):
        return
    
    await client.interaction_component_acknowledge(event, wait = False)
    
    entity_id, entity = await choice_type.parse_and_get_entity_id_and_entity(client, event)
    if entity is None:
        return
    
    components = translate_components(event.message.iter_components(), ACTIONS_DISABLE)
    components.append(Row(*choice_type.iter_action_components(entity, event)))
    
    await client.interaction_response_message_edit(
        event,
        components = components,
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ACTIONS_EMOJI)
async def snipe_interaction_actions_emoji(client, event):
    """
    Adds the possible actions to the message as additional operations.
    
    > Emoji version.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await respond_with_actions(client, event,
        ChoiceTypeEmoji)

@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ACTIONS_SOUNDBOARD_SOUND)
async def snipe_interaction_actions_soundboard_sound(client, event):
    """
    Adds the possible actions to the message as additional operations.
    
    > SoundboardSound version.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await respond_with_actions(client, event, ChoiceTypeSoundboardSound)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ACTIONS_STICKER)
async def snipe_interaction_actions_sticker(client, event):
    """
    Adds the possible actions to the message as additional operations.
    
    > Sticker version.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await respond_with_actions(client, event, ChoiceTypeSticker)
