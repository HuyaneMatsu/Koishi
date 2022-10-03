__all__ = ()

from hata import Client
from hata.ext.slash import Button

from ...constants import EMOJI_NEW
from ...image_handler import ImageHandlerMeekMoe


from .vocaloid import NewVocaloid, VOCALOID_CHARACTERS, make_custom_id_of_vocaloid, build_vocaloid_embed


SLASH_CLIENT : Client


HANDLERS = {character: ImageHandlerMeekMoe(character) for character in VOCALOID_CHARACTERS.values()}


@SLASH_CLIENT.interactions(is_global=True)
async def vocaloid(
    client,
    event,
    character : (VOCALOID_CHARACTERS, 'Select a character!') = 'miku',
):
    """Ayaya."""
    handler = HANDLERS[character]
    image_detail = await handler.get_image(client, event)
    
    embed = build_vocaloid_embed(character, image_detail)
    
    if (image_detail is None):
        components = None
    else:
        components = Button(
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
    SLASH_CLIENT.interactions(
        NewVocaloid(handler, character),
        custom_id = make_custom_id_of_vocaloid(character),
    )

character = None
handler = None

del character
del handler
