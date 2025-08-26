__all__ = ()

from hata import create_button

from ...bots import FEATURE_CLIENTS

from ..image_handling_core import ImageHandlerMeekMoe

from .constants import EMOJI_NEW
from .vocaloid import NewVocaloid, VOCALOID_CHARACTERS, make_custom_id_of_vocaloid, build_vocaloid_embed


HANDLERS = {character: ImageHandlerMeekMoe(character) for character in VOCALOID_CHARACTERS.values()}


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def vocaloid(
    client,
    event,
    character : (VOCALOID_CHARACTERS, 'Select a character!') = 'miku',
):
    """Baka Baka Baka"""
    handler = HANDLERS[character]
    
    cg_get_image = handler.cg_get_image()
    
    try:
        image_detail = await cg_get_image.asend(None)
        if (image_detail is None):
            await client.interaction_application_command_acknowledge(event, False)
            image_detail = await cg_get_image.asend(None)
        
    except StopAsyncIteration:
        image_detail = None
    
    finally:
        cg_get_image.aclose().close()
    
    embed = build_vocaloid_embed(character, image_detail)
    
    if (image_detail is None):
        components = None
    else:
        components = create_button(
            emoji = EMOJI_NEW,
            custom_id = make_custom_id_of_vocaloid(character),
        )
    
    if event.is_unanswered():
        function = type(client).interaction_response_message_create
    else:
        function = type(client).interaction_response_message_edit
    
    await function(
        client,
        event,
        embed = embed,
        components = components,
    )


for character, handler in HANDLERS.items():
    FEATURE_CLIENTS.interactions(
        NewVocaloid(handler, character),
        custom_id = make_custom_id_of_vocaloid(character),
    )

character = None
handler = None

del character
del handler
