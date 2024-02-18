import vampytest
from hata import DATETIME_FORMAT_CODE, Channel, ChannelType, Message, MessageType, User, id_to_datetime 

from ..constants import MESSAGE_RENDER_MODE_CREATE
from ..solution_builders import build_message_common_description


def test__build_message_common_description():
    """
    Tests whether ``build_message_common_description`` works as intended.
    """
    channel_name = 'orin'
    user_name = 'okuu'
    channel_type = ChannelType.guild_text
    channel_id = 202401310002
    message_id = 202401310003
    user_id = 202401310004
    content = 'hey mister'
    user = User.precreate(user_id, name = user_name)
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = channel_name)
    message_type = MessageType.call
    title = 'satori'
    
    message = Message.precreate(
        message_id,
        author = user,
        channel = channel,
        content = content,
        message_type = message_type,
    )
    
    output = build_message_common_description(message, MESSAGE_RENDER_MODE_CREATE, title = title)

    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'### {title!s}\n'
            f'\n'
            f'Id: {message_id!s}\n'
            f'Type: {message_type.name!s} ~ {message_type.value}\n'
            f'Created: {id_to_datetime(message_id):{DATETIME_FORMAT_CODE}}\n'
            f'Length: {len(content)!s}\n'
            f'Author: {user_name!s} ({user_id!s})\n'
            f'Channel: {channel_name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})'
        ),
    )
