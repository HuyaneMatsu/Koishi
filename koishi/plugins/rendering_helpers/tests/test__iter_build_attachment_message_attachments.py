import vampytest
from hata import Attachment, Message
from scarletio import get_event_loop
from scarletio.http_client import HTTPClient
from scarletio.streaming import ZipStreamFile, create_zip_stream_resource

from ....bot_utils.response_data_streaming import create_http_stream_resource

from ..attachment_builders import iter_build_attachment_message_attachments


async def test__iter_build_attachment_message_attachments__no_attachments():
    """
    tests whether ``iter_build_attachment_message_attachments`` works as intended.
    
    This function is a coroutine.
    
    Case: No attachments.
    """
    http = HTTPClient(get_event_loop())
    
    message = Message.precreate(
        202503070000,
        attachments = None,
    )
    
    output = [*iter_build_attachment_message_attachments(http, message)]
    vampytest.assert_eq(len(output), 0)


async def test__iter_build_attachment_message_attachments__with_attachments():
    """
    tests whether ``iter_build_attachment_message_attachments`` works as intended.
    
    This function is a coroutine.
    
    Case: With content.
    """
    http = HTTPClient(get_event_loop())
    
    attachment_0 = Attachment.precreate(202503070002_000000, name = 'sister.txt', size = 12)
    
    message = Message.precreate(
        202503070001,
        attachments = (attachment_0,),
    )
    
    output = [*iter_build_attachment_message_attachments(http, message)]
    vampytest.assert_eq(len(output), 1)
    
    vampytest.assert_eq(
        output[0],
        (
            'attachments.zip',
            create_zip_stream_resource([
                ZipStreamFile(
                    attachment_0.display_name,
                    create_http_stream_resource(http, attachment_0.url),
                    modified_at = attachment_0.content_created_at,
                ),
            ]),
        )
    )
