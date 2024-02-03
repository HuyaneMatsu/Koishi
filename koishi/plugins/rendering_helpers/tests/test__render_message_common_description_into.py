from datetime import timedelta as TimeDelta

import vampytest
from hata import DATETIME_FORMAT_CODE, Channel, ChannelType, Message, MessageType, User, id_to_datetime 

from ..constants import MESSAGE_RENDER_MODE_CREATE, MESSAGE_RENDER_MODE_DELETE
from ..solution_renderers import render_message_common_description_into

from .mocks import DateTimeMock, is_instance_mock


def test__render_message_common_description_into__create():
    """
    Tests whether ``render_message_common_description_into`` works as intended.
    
    Case: create.
    """
    channel_name = 'orin'
    user_name = 'okuu'
    channel_type = ChannelType.guild_text
    channel_id = 202401020000
    message_id = 202401020001
    user_id = 202401020003
    content = 'hey mister'
    user = User.precreate(user_id, name = user_name)
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = channel_name)
    message_type = MessageType.call
    
    message = Message.precreate(
        message_id,
        author = user,
        channel = channel,
        content = content,
        message_type = message_type,
    )
    
    field_added = False
    
    into, field_added = render_message_common_description_into(
        [], field_added, message, MESSAGE_RENDER_MODE_CREATE, None
    )
    vampytest.assert_instance(into, list)
    vampytest.assert_instance(field_added, bool)
    output = ''.join(into)
    vampytest.assert_eq(
        output,
        (
            f'Id: {message_id!s}\n'
            f'Type: {message_type.name!s} ~ {message_type.value}\n'
            f'Created: {id_to_datetime(message_id):{DATETIME_FORMAT_CODE}}\n'
            f'Length: {len(content)!s}\n'
            f'Author: {user_name!s} ({user_id!s})\n'
            f'Channel: {channel_name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})'
        ),
    )
    vampytest.assert_eq(field_added, True)


def test__render_message_common_description_into__delete_title():
    """
    Tests whether ``render_message_common_description_into`` works as intended.
    
    Case: delete & title
    """
    channel_name = 'orin'
    user_name = 'okuu'
    channel_type = ChannelType.guild_text
    channel_id = 202402020006
    message_id = 202402020007
    user_id = 202402020008
    content = 'hey mister'
    user = User.precreate(user_id, name = user_name)
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = channel_name)
    message_type = MessageType.call
    current_date_time = id_to_datetime(message_id) + TimeDelta(seconds = 20)
    DateTimeMock.set_current(current_date_time)
    title = 'satori'
    
    message = Message.precreate(
        message_id,
        author = user,
        channel = channel,
        content = content,
        message_type = message_type,
    )
    
    field_added = False
    
    mocked = vampytest.mock_globals(
        render_message_common_description_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked([], field_added, message, MESSAGE_RENDER_MODE_DELETE, title)
    vampytest.assert_instance(into, list)
    vampytest.assert_instance(field_added, bool)
    output = ''.join(into)
    vampytest.assert_eq(
        output,
        (
            f'### {title!s}\n'
            f'\n'
            f'Id: {message_id!s}\n'
            f'Type: {message_type.name!s} ~ {message_type.value}\n'
            f'Created: {id_to_datetime(message_id):{DATETIME_FORMAT_CODE}} [*20 seconds ago*]\n'
            f'Deleted: {current_date_time:{DATETIME_FORMAT_CODE}}\n'
            f'Length: {len(content)!s}\n'
            f'Author: {user_name!s} ({user_id!s})\n'
            f'Channel: {channel_name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})'
        ),
    )
    vampytest.assert_eq(field_added, True)
