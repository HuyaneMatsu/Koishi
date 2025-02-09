from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Channel, Client, Component, ComponentType, DATETIME_FORMAT_CODE, DiscordApiClient, DiscordException, ERROR_CODES,
    Embed, Message, Poll, PollAnswer, User, Webhook, create_row, id_to_datetime
)
from scarletio.web_common import FormData

from ..create import create_webhook_message


class TestDiscordApiClient(DiscordApiClient):
    __slots__ = ('__dict__',)
    
    async def discord_request(self, handler, method, url, data = None, query = None, headers = None, reason = None):
        raise RuntimeError('Real request during testing.')


async def test__create_webhook_message__stuffed():
    """
    Tests whether ``create_webhook_message`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202405030002
    channel_id = 202405030003
    message_id = 202405030004
    message_id_0 = 202405030005
    message_id_1 = 202405030006
    webhook_id = 202405030007
    thread_id = 202405030008
    user_id = 202405030009
    webhook_token = 'reisen'
    user_name = 'satori'
    
    mock_api_webhook_message_create_call_counter = 0
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    user = User.precreate(user_id, name = user_name)
    
    files = [('mister.txt', b'hey', None)]
    components = [create_row(Component(ComponentType.button, label = 'koishi', custom_id = 'satori'))]
    content = 'suika' * 600
    embeds = [Embed('orin')]
    poll = Poll(answers = [PollAnswer(text = 'sister')], expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    message = Message.precreate(
        message_id,
        author = user,
        components = components,
        content = content,
        embeds = embeds,
        poll = poll,
    )
    
    expected_message_data_0 = {
        'content': content[:2000],
        'avatar_url': user.avatar_url,
        'username': f'{user_name} - {id_to_datetime(message_id):{DATETIME_FORMAT_CODE}}',
        'allowed_mentions': {'parse': []},
    }
    
    expected_message_data_1 = FormData()
    expected_message_data_1.add_json(
        'payload_json',
        {
            'content': content[2000:],
            'embeds': [embed.to_data() for embed in embeds],
            'poll': poll.copy_with(duration = 3600).to_data(),
            # 'components': [component.to_data() for component in components],
            'allowed_mentions' : {'parse': []},
            'attachments': [{'id': '0'}],
            'avatar_url': user.avatar_url,
            'username': f'{user_name} - {id_to_datetime(message_id):{DATETIME_FORMAT_CODE}}',
        },
    )
    expected_message_data_1.add_field(
        f'files[{0}]', b'hey', file_name = 'mister.txt', content_type = 'application/octet-stream'
    )
    
    return_message_data_0 = {
        'id': str(message_id_0),
        'channel_id': str(channel_id)
    }
    
    return_message_data_1 = {
        'id': str(message_id_1),
        'channel_id': str(channel_id),
    }
    
    async def mock_api_webhook_message_create(
        input_webhook_id, input_webhook_token, input_message_data, input_query_parameters
    ):
        nonlocal mock_api_webhook_message_create_call_counter
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data_0
        nonlocal return_message_data_0
        nonlocal return_message_data_1
        nonlocal expected_message_data_1
        nonlocal thread_id
        
        if mock_api_webhook_message_create_call_counter == 0:
            expected_message_data = expected_message_data_0
            return_message_data = return_message_data_0
        elif mock_api_webhook_message_create_call_counter == 1:
            expected_message_data = expected_message_data_1
            return_message_data = return_message_data_1
        else:
            expected_message_data = None
            return_message_data = None
        
        mock_api_webhook_message_create_call_counter += 1
        
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq({'thread_id': str(thread_id), 'with_components': True}, input_query_parameters)
        return return_message_data
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        await create_webhook_message(client, webhook, message, thread_id, files)
        vampytest.assert_eq(mock_api_webhook_message_create_call_counter, 2)
    
    finally:
        client._delete()
        client = None


async def test__create_webhook_message__empty():
    """
    Tests whether ``create_webhook_message`` works as intended.
    
    Case: empty message.
    
    This function is a coroutine.
    """
    client_id = 202405030010
    channel_id = 202405030011
    message_id = 202405030012
    webhook_id = 202405030013
    thread_id = 202405030014
    user_id = 202405030015
    webhook_token = 'reisen'
    user_name = 'reisen'
    
    mock_api_webhook_message_create_call_counter = 0
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    user = User.precreate(user_id, name = user_name)
    
    # components are ignored, so we can pass them through the check
    components = [create_row(Component(ComponentType.button, label = 'koishi', custom_id = 'satori'))]
    
    message = Message.precreate(
        message_id,
        author = user,
        components = components,
    )
    
    async def mock_api_webhook_message_create(
        input_webhook_id, input_webhook_token, input_message_data, input_query_parameters
    ):
        nonlocal mock_api_webhook_message_create_call_counter
        mock_api_webhook_message_create_call_counter += 1
        
        exception = DiscordException(None, None, None, None)
        exception.code = ERROR_CODES.cannot_create_empty_message
        raise exception
    
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        await create_webhook_message(client, webhook, message, thread_id, None)
        vampytest.assert_eq(mock_api_webhook_message_create_call_counter, 1)
    
    finally:
        client._delete()
        client = None
