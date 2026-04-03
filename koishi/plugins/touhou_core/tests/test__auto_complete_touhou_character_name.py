import vampytest
from hata import Client, InteractionEvent, InteractionType

from ..auto_completion import auto_complete_touhou_character_name


def _iter_options():
    yield (
        202508200000,
        202508200001,
        None,
        [
            'Komeiji Koishi',
            'Kirisame Marisa',
            'Hakurei Reimu',
            'Scarlet Flandre',
            'Izayoi Sakuya',
            'Scarlet Remilia',
            'Fujiwara no Mokou',
            'Komeiji Satori',
            'Saigyouji Yuyuko',
            'Shameimaru Aya',
            'Margatroid Alice',
            'Kochiya Sanae',
            'Reisen Udongein Inaba',
            'Hinanawi Tenshi',
            'Yakumo Yukari',
            'Hata no Kokoro',
            'Chiruno',
            'Patchouli Knowledge',
            'Tatara Kogasa',
            'Rumia',
            'Moriya Suwako',
            'Shiki Eiki Yamaxanadu',
            'Kazami Yuuka',
            'Hong Meiling',
            'Toyosatomimi no Miko',
        ],
    )
    
    yield (
        202508200002,
        202508200003,
        'y',
        [
            'yachie',
            'yagokoro eirin',
            'yakumo ran',
            'yakumo yukari',
            'yamame',
            'yamashiro takane',
            'yasaka kanako',
            'yatadera narumi',
            'yatsuhashi tsukumo',
            'yomotsu hisami',
            'yorigami joon',
            'yorigami shion',
            'yorihime',
            'yorumi',
            'yoshika',
            'youki konpaku',
            'youmu',
            'yuiman asama',
            'yuki',
            'yumeko',
            'yumemi okazaki',
            'yuugen magan',
            'yuugi',
            'yuuka',
            'yuuma',
        ]
    )
    
    yield (
        202508200004,
        202508200005,
        'aya',
        [
            'aya',
            'ayana',
            'layla',
            'ariya',
            'haniyasushin keiki',
            'kagiyama hina',
            'kaguya',
            'ran yakumo',
            'sakuya',
            'yukari yakumo',
            'kurodani yamame',
            'yoshika miyako',
            'kanako yasaka',
            'narumi yatadera',
            'takane yamashiro',
            'sannyo komakusa',
            'suwako moriya',
            'tenkajin chiyari',
            'asama yuiman',
            'kazami yuuka',
            'sanae kochiya',
            'sukuna shinmyoumaru',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__auto_complete_touhou_character_name(client_id, interaction_event_id, value):
    """
    Tests whether ``auto_complete_touhou_character_name`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client_id : `int`
        Client identifier to test with.
    
    interaction_event_id : `int`
        Interaction event identifier to test with.
    
    value : `None | str`
        The value to autocomplete.
    
    Returns
    -------
    output : `list<str>`
    """
    suggestions = None
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    original_interaction_application_command_autocomplete = Client.interaction_application_command_autocomplete
    
    try:
        
        interaction_event = InteractionEvent.precreate(
            interaction_event_id,
            interaction_type = InteractionType.application_command_autocomplete,
        )
        
        async def patch_interaction_application_command_autocomplete(
            input_client,
            input_interaction_event,
            input_suggestions,
        ):
            nonlocal client
            nonlocal interaction_event
            nonlocal suggestions
            
            vampytest.assert_is(input_client, client)
            vampytest.assert_is(input_interaction_event, interaction_event)
            suggestions = input_suggestions
        
        Client.interaction_application_command_autocomplete = patch_interaction_application_command_autocomplete
        
        await auto_complete_touhou_character_name(client, interaction_event, value)
    
    finally:
        Client.interaction_application_command_autocomplete = original_interaction_application_command_autocomplete
        client._delete()
        client = None
    
    return suggestions
