import vampytest
from hata import Emoji, Message, ReactionAddEvent, ReactionType, User

from ..embed_builder_reaction import _build_reaction_description


def test__build_reaction_description():
    """
    Tests whether ``_build_reaction_description`` works as intended.
    """
    emoji_id = 202404280017
    emoji_name = 'sister'
    message_id = 202404280018
    user_id = 202404280019
    reaction_type = ReactionType.burst
    
    emoji = Emoji.precreate(emoji_id, name = emoji_name)
    message = Message.precreate(message_id)
    user = User.precreate(user_id)
    event = ReactionAddEvent(message, emoji, user, reaction_type = reaction_type)
    
    output =_build_reaction_description(event)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'Type: {reaction_type.name!s} ~ {reaction_type.value!r}\n'
            f'Emoji: {emoji_name!s} ({emoji_id!s})'
        ),
    )
