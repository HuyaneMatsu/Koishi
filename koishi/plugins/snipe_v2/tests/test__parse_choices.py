import vampytest

from hata import (
    Emoji, InteractionEvent, InteractionType, Message, SoundboardSound, Sticker, StringSelectOption, User, create_row,
    create_string_select
)

from ..custom_ids import CUSTOM_ID_SNIPE_CHOICE_BUILDER
from ..entity_packing import pack_entity
from ..responding_helpers import parse_choices


def _iter_options():
    user_id = 202511020000
    emoji_id_0 = 202511020001
    emoji_id_1 = 202511020002
    guild_id_0 = 202511020003
    guild_id_1 = 202511020004
    message_id = 202511020005
    interaction_event_id = 202511020006
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        guild_id = guild_id_0,
        name = 'shrimp',
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        guild_id = guild_id_1,
        name = 'fry',
    )
    
    user = User.precreate(
        user_id,
    )
    
    feature_flags = 2
    
    yield (
        InteractionEvent.precreate(
            interaction_event_id,
            interaction_type = InteractionType.message_component,
            message = Message.precreate(
                message_id,
                components = [
                    create_row(
                        create_string_select(
                            [
                                StringSelectOption(pack_entity(emoji_0), emoji_0.name),
                                StringSelectOption(pack_entity(emoji_1), emoji_1.name),
                            ],
                            CUSTOM_ID_SNIPE_CHOICE_BUILDER(user_id, feature_flags),
                        ),
                    ),
                ],
            ),
            user = user,
        ),
        user_id,
        feature_flags,
        [
            emoji_0,
            emoji_1,
        ],
        [
            emoji_0,
            emoji_1,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_choices(interaction_event, user_id, feature_flags, entity_cache):
    """
    tests whether ``parse_choices`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `int`
        The original invoking user's identifier as hexadecimal integer.
    
    feature_flags : `int`
        The current feature flags of the snipe as hexadecimal string.
    
    entity_cache : `list<object>`
        Additional entities to keep cached.
    
    Returns
    -------
    output : ``None | list<Emoji, Sticker, SoundboardSound>``
    """
    output = parse_choices(interaction_event, user_id, feature_flags)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Emoji, Sticker, SoundboardSound)
    
    return output
