__all__ = ()

from hata import Client
from hata.ext.slash import Button, abort

from ...touhou_core import (
    TOUHOU_CHARACTERS_UNIQUE, TouhouHandlerKey, get_touhou_character_like, get_touhou_character_names_like
)
from ...touhou_core.characters import (
    CHIRUNO, FUJIWARA_NO_MOKOU, HAKUREI_REIMU, HATA_NO_KOKORO, HINANAWI_TENSHI, HONG_MEILING, IZAYOI_SAKUYA,
    KAZAMI_YUUKA, KIRISAME_MARISA, KOCHIYA_SANAE, KOMEIJI_KOISHI, KOMEIJI_SATORI, MARGATROID_ALICE, MORIYA_SUWAKO,
    PATCHOULI_KNOWLEDGE, REISEN_UDONGEIN_INABA, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SCARLET_REMILIA,
    SHAMEIMARU_AYA, SHIKI_EIKI_YAMAXANADU, TATARA_KOGASA, TOYOSATOMIMI_NO_MIKO, YAKUMO_YUKARI
)

from ..constants import EMOJI_NEW

from .touhou_character import (
    NewTouhouCharacter, build_no_match_embed, build_touhou_character_embed, make_custom_id_of_character
)


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(is_global = True)
async def touhou_character(
    client,
    event,
    name: ('str', 'Who\'s?'),
):
    """Shows you the given Touhou character's portrait."""
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


POPULAR_TOUHOU_CHARACTER_NAMES = [
    KOMEIJI_KOISHI.name,
    KIRISAME_MARISA.name,
    HAKUREI_REIMU.name,
    SCARLET_FLANDRE.name,
    IZAYOI_SAKUYA.name,
    SCARLET_REMILIA.name,
    FUJIWARA_NO_MOKOU.name,
    KOMEIJI_SATORI.name,
    SAIGYOUJI_YUYUKO.name,
    SHAMEIMARU_AYA.name,
    MARGATROID_ALICE.name,
    KOCHIYA_SANAE.name,
    REISEN_UDONGEIN_INABA.name,
    HINANAWI_TENSHI.name,
    YAKUMO_YUKARI.name,
    HATA_NO_KOKORO.name,
    CHIRUNO.name,
    PATCHOULI_KNOWLEDGE.name,
    TATARA_KOGASA.name,
    RUMIA.name,
    MORIYA_SUWAKO.name,
    SHIKI_EIKI_YAMAXANADU.name,
    KAZAMI_YUUKA.name,
    HONG_MEILING.name,
    TOYOSATOMIMI_NO_MIKO.name,
]


@touhou_character.autocomplete('name')
async def auto_complete_touhou_character_name(name):
    if name is None:
        touhou_character_names = POPULAR_TOUHOU_CHARACTER_NAMES
    else:
        touhou_character_names = get_touhou_character_names_like(name)
    
    return touhou_character_names



for touhou_character in TOUHOU_CHARACTERS_UNIQUE:
    SLASH_CLIENT.interactions(
        NewTouhouCharacter(TouhouHandlerKey(touhou_character, solo = True).get_handler(), touhou_character),
        custom_id = make_custom_id_of_character(touhou_character),
    )

touhou_character = None

del touhou_character
