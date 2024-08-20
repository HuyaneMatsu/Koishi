__all__ = ()

from hata.ext.slash import Button, P, abort

from ...bots import FEATURE_CLIENTS

from ..touhou_core import (
    TOUHOU_CHARACTERS, TouhouHandlerKey, auto_complete_touhou_character_name, get_touhou_character_like
)

from .constants import EMOJI_NEW
from .touhou_character import (
    NewTouhouCharacter, build_no_match_embed, build_touhou_character_embed, make_custom_id_of_character
)


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def touhou_character(
    client,
    event,
    name: P('str', 'Who\'s?', autocomplete = auto_complete_touhou_character_name),
):
    """
    Shows you the given Touhou character's portrait.
    
    This function is a coroutine.
    
    Parameters
    ----------
    name : `str`
        the character's name.
    """
    name_length = len(name)
    if name_length == 0:
        abort('Empty name was given.')
    
    touhou_character = get_touhou_character_like(name)
    if (touhou_character is None):
        return build_no_match_embed(name)
    
    handler = TouhouHandlerKey(touhou_character, solo = True).get_handler()
    image_detail = await handler.get_image(client, event)
    
    embed = build_touhou_character_embed(touhou_character, image_detail)
    
    if image_detail is None:
        components = None
    else:
        components = Button(
            emoji = EMOJI_NEW,
            custom_id = make_custom_id_of_character(touhou_character),
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


for touhou_character in TOUHOU_CHARACTERS.values():
    FEATURE_CLIENTS.interactions(
        NewTouhouCharacter(TouhouHandlerKey(touhou_character, solo = True).get_handler(), touhou_character),
        custom_id = make_custom_id_of_character(touhou_character),
    )

touhou_character = None

del touhou_character
