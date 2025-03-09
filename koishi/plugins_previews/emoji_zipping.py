__all__ = ()

from hata import parse_custom_emojis
from hata.ext.slash import InteractionResponse, abort
from scarletio.streaming import ZipStreamFile, create_zip_stream_resource

from ..bot_utils.response_data_streaming import create_http_stream_resource
from ..bots import FEATURE_CLIENTS


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    target = 'message',
)
async def zip_emojis(client, message):
    """Zips the emojis into an archive and uploads them back."""
    content = message.content
    if not content:
        abort('Empty message')
    
    emojis = parse_custom_emojis(content)
    if not emojis:
        abort('No custom emojis.')
    
    return InteractionResponse(
        file = (
            'emojis.zip',
            create_zip_stream_resource(
                ZipStreamFile(
                    f'{emoji.name}_{emoji.id}.{"gif" if emoji.animated else "png"}',
                    create_http_stream_resource(client.http, emoji.url),
                )
                for emoji in sorted(emojis)
            ),
        )
    )
