from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Attachment
from scarletio import get_event_loop
from scarletio.http_client import HTTPClient
from scarletio.streaming import ZipStreamFile, create_zip_stream_resource

from ....bot_utils.response_data_streaming import create_http_stream_resource

from ..attachment_builders import _build_attachment_attachments


async def test__build_attachment_attachments():
    """
    Tests whether ``_build_attachment_attachments`` works as intended.
    
    This function is a coroutine.
    """
    date_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    attachment_0 = Attachment.precreate(202503060009_000000, clip_created_at = date_0, name = 'sister.txt', size = 12)
    attachment_1 = Attachment.precreate(202503060010_000000, name = 'mister.txt', size = 13, title = 'miau')
    attachment_2 = Attachment.precreate(202503060011_000000, name = 'kisser.txt', size = 14)
    
    http = HTTPClient(get_event_loop())
    
    output = _build_attachment_attachments(http, (attachment_0, attachment_1, attachment_2), 2)
    vampytest.assert_eq(
        output,
        (
            'attachments.zip',
            create_zip_stream_resource([
                ZipStreamFile(
                    attachment_0.display_name,
                    create_http_stream_resource(http, attachment_0.url),
                    modified_at = attachment_0.content_created_at,
                ),
                ZipStreamFile(
                    attachment_1.display_name,
                    create_http_stream_resource(http, attachment_1.url),
                    modified_at = attachment_1.content_created_at,
                ),
            ]),
        )
    )
