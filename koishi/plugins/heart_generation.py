__all__ = ()

from random import random

from hata import InteractionType, KOKORO

from ..bots import FEATURE_CLIENTS

from .user_balance import user_balance_get, user_balance_save, user_balance_modify_balance_by


HEART_GENERATOR_COOLDOWNS = set()
HEART_GENERATOR_COOLDOWN = 3600.0
HEART_GENERATION_AMOUNT = 50

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE = InteractionType.application_command_autocomplete


# yup, we are generating hearts
@FEATURE_CLIENTS.events(name = 'interaction_create')
async def heart_generator(client, event):
    user_id = event.user.id
    if user_id in HEART_GENERATOR_COOLDOWNS:
        return
    
    event_type = event.type
    if event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
        chance = 0.05
    elif event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
        chance = 0.01
    elif event_type is INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE:
        chance = 0.005
    else:
        return
    
    if random() >= chance:
        return
    
    KOKORO.call_after(HEART_GENERATOR_COOLDOWN, set.discard, HEART_GENERATOR_COOLDOWNS, user_id)
    user_balance = await user_balance_get(user_id)
    user_balance_modify_balance_by(user_balance, HEART_GENERATION_AMOUNT)
    await user_balance_save(user_balance)
