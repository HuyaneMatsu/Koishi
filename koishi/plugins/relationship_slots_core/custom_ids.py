__all__ = ('CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_RP',)

from re import compile as re_compile

# invoke
CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_BUILDER = (
    lambda user_id: f'user.buy_relationship_slots.invoke.{user_id:x}'
)
CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_RP = re_compile(
    f'user\\.buy_relationship_slots\\.invoke\\.([0-9a-f]+)'
)
