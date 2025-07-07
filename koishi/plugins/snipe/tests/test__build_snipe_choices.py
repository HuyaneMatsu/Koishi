import vampytest
from hata import Emoji, Message, MessageSnapshot, ReactionMapping, ReactionMappingLine, Sticker, User

from ..choice import Choice
from ..choice_type import ChoiceTypeEmoji, ChoiceTypeReaction, ChoiceTypeSticker
from ..command_helpers_snipe_whole_message import _build_snipe_choices


def _iter_options():
    emoji_0 = Emoji.precreate(202506200015, name = 'AyaSmile')
    emoji_1 = Emoji.precreate(202506200016, name = 'AyaSad')
    emoji_2 = Emoji.precreate(202506200017, name = 'AyaHug')
    
    sticker_0 = Sticker.precreate(202506200011, name = 'AyaCry')
    sticker_1 = Sticker.precreate(202506200012, name = 'AyaSatisfied')
    sticker_2 = Sticker.precreate(202506200013, name = 'AyaYa')
    
    user_0 = User.precreate(202506200021, name = 'Aya')
    
    message = Message.precreate(202506200010)
    
    yield (
        'empty',
        message,
        [],
    )
    
    message = Message.precreate(
        202506200014,
        stickers = [sticker_0, sticker_1, sticker_2],
    )
    
    yield (
        'stickers',
        message,
        [
            Choice(sticker_0, ChoiceTypeSticker),
            Choice(sticker_1, ChoiceTypeSticker),
            Choice(sticker_2, ChoiceTypeSticker),
        ],
    )
    
    message = Message.precreate(
        202506200018,
        content = f'{emoji_0} {emoji_1} {emoji_2}'
    )
    
    yield (
        'emojis',
        message,
        [
            Choice(emoji_0, ChoiceTypeEmoji),
            Choice(emoji_1, ChoiceTypeEmoji),
            Choice(emoji_2, ChoiceTypeEmoji),
        ],
    )
    
    message = Message.precreate(
        202506200019,
        snapshots = [
            MessageSnapshot(
                content = f'{emoji_0} {emoji_1} {emoji_2}'
            ),
        ],
    )
    
    yield (
        'snapshot emojis',
        message,
        [
            Choice(emoji_0, ChoiceTypeEmoji),
            Choice(emoji_1, ChoiceTypeEmoji),
            Choice(emoji_2, ChoiceTypeEmoji),
        ],
    )
    
    message = Message.precreate(
        202506200020,
        reactions = ReactionMapping(
            lines = {
                emoji_0 : ReactionMappingLine(users = [user_0]),
                emoji_1 : ReactionMappingLine(users = [user_0]),
                emoji_2 : ReactionMappingLine(users = [user_0]),
            },
        ),
    )
    
    yield (
        'reactions',
        message,
        [
            Choice(emoji_0, ChoiceTypeReaction),
            Choice(emoji_1, ChoiceTypeReaction),
            Choice(emoji_2, ChoiceTypeReaction),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__build_snipe_choices(message):
    """
    Tests whether ``_build_snipe_choices`` works as intended.
    
    Parameters
    ----------
    message : ``Message``
        The sniped message.
    
    Returns
    -------
    output : ``list<ChoiceBase>``
    """
    output = _build_snipe_choices(message)
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, Choice)
    
    return output
