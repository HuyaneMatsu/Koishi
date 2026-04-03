import vampytest
from hata import Emoji, Message, MessageSnapshot, ReactionMapping, ReactionMappingLine, SoundboardSound, Sticker

from ..responding_helpers import get_entity_and_choices_of_message


def _iter_options():
    message = Message.precreate(
        202511010020,
    )
    
    yield (
        message,
        (
            None,
            None,
        ),
    )
    
    soundboard_sound = SoundboardSound.precreate(
        202511010021,
    )
    
    message = Message.precreate(
        202511010022,
        soundboard_sounds = [
            soundboard_sound,
        ],
    )
    
    yield (
        message,
        (
            soundboard_sound,
            None,
        ),
    )
    
    sticker = Sticker.precreate(
        202511010023,
    )
    
    message = Message.precreate(
        202511010024,
        stickers = [
            sticker,
        ],
    )
    
    yield (
        message,
        (
            sticker,
            None,
        ),
    )
    
    emoji = Emoji.precreate(
        202511010025,
        name = 'KoishiStare',
    )
    
    message = Message.precreate(
        202511010026,
        content = f'{emoji}',
    )
    
    yield (
        message,
        (
            emoji,
            None,
        ),
    )
    
    emoji = Emoji.precreate(
        202511010027,
    )
    
    message = Message.precreate(
        202511010028,
        reactions = ReactionMapping(
            lines = {
                emoji : ReactionMappingLine(count = 1),
            },
        ),
    )
    
    yield (
        message,
        (
            emoji,
            None,
        ),
    )
    
    # Test snapshot
    
    emoji = Emoji.precreate(
        202511010029,
        name = 'KoishiStare',
    )
    
    message = Message.precreate(
        202511010030,
        snapshots = [
            MessageSnapshot(
                content = f'{emoji}',
            ),
        ],
    )
    
    yield (
        message,
        (
            emoji,
            None,
        ),
    )
    
    # Test multiple choice & deduplication
    
    emoji_0 = Emoji.precreate(
        202511010031,
        name = 'KoishiStare',
    )
    emoji_1 = Emoji.precreate(
        202511010032,
        name = 'KoishiHug',
    )
    
    message = Message.precreate(
        202511010033,
        content = f'{emoji_0} {emoji_1}',
        reactions = ReactionMapping(
            lines = {
                emoji_0 : ReactionMappingLine(count = 1),
            },
        ),
    )
    
    yield (
        message,
        (
            emoji_0,
            [
                emoji_0,
                emoji_1,
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_entity_and_choices_of_message(message):
    """
    Tests whether ``get_entity_and_choices_of_message`` works as intended.
    
    Parameters
    ----------
    message : ``Message``
        The received message.
    
    Returns
    -------
    output : ``(None | Emoji | Sticker | SoundboardSound, None | list<Emoji | Sticker | SoundboardSound>)``
    """
    output = get_entity_and_choices_of_message(message)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    entity, choices = output
    vampytest.assert_instance(entity, Emoji, Sticker, SoundboardSound, nullable = True)
    
    vampytest.assert_instance(choices, list, nullable = True)
    if (choices is not None):
        for element in choices:
            vampytest.assert_instance(element, Emoji, Sticker, SoundboardSound)
    
    return output
