__all__ = ('auto_complete_touhou_character_name',)

from hata import DiscordException, ERROR_CODES

from .characters import (
    CHIRUNO, FUJIWARA_NO_MOKOU, HAKUREI_REIMU, HATA_NO_KOKORO, HINANAWI_TENSHI, HONG_MEILING, IZAYOI_SAKUYA,
    KAZAMI_YUUKA, KIRISAME_MARISA, KOCHIYA_SANAE, KOMEIJI_KOISHI, KOMEIJI_SATORI, MARGATROID_ALICE, MORIYA_SUWAKO,
    PATCHOULI_KNOWLEDGE, REISEN_UDONGEIN_INABA, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SCARLET_REMILIA,
    SHAMEIMARU_AYA, SHIKI_EIKI_YAMAXANADU, TATARA_KOGASA, TOYOSATOMIMI_NO_MIKO, YAKUMO_YUKARI
)
from .utils import get_touhou_character_names_like


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


async def auto_complete_touhou_character_name(client, interaction_event, name):
    """
    Auto completes touhou character name based on the given input.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `None | str`
        Input of the user.
    """
    if name is None:
        suggestions = POPULAR_TOUHOU_CHARACTER_NAMES
    else:
        suggestions = get_touhou_character_names_like(name)
    
    try:
        await client.interaction_application_command_autocomplete(
            interaction_event,
            suggestions,
        )
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (exception.code != ERROR_CODES.unknown_interaction)
        ):
            raise
