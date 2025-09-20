__all__ = ()

import sys
from os.path import join as join_paths

from hata import KOKORO, parse_signed_url
from hata.ext.plugin_loader import import_plugin
from hata.main import register
from scarletio import ReuAsyncIO

from ..action_asset_format_converter.constants import ASSETS_DIRECTORY
from ..action_asset_format_converter.grouping import read_asset_entries

from .filtering import (
    classify_asset_entry_parts, filter_new_asset_entries, get_image_detail_names, get_image_detail_tags
)
from .rendering import get_producer_for


async def upload(client, asset_entry, channel_id):
    """
    Uploads the given asset entry.
    
    Parameters
    ----------
    client : ``Client``
        Client to upload the entry with.
    
    asset_entry : ``AssetEntry``
        The asset entry to upload.
    
    channel_id : `int`
        The channel's identifier to upload to.
    
    Returns
    -------
    message : ``Message``
    """
    with await ReuAsyncIO(join_paths(ASSETS_DIRECTORY, asset_entry.reconstruct_file_name())) as file:
        return await client.message_create(channel_id, file = file)


@register
def upload_action_assets(
    creator : str = None,
):
    """
    Uploads the not yet uploaded action assets.
    
    Produces a long a text that can be copy pasted. Entries not known how to handled will get a `TODO` mark.
    """
    # import plugins
    import_plugin(__package__[: __package__.find('.')] + '.plugins')
    
    from ...bots.koishi import Koishi
    from ...plugins.image_commands_actions import TOUHOU_ACTION_ALL
    from ...plugins.touhou_core import get_touhou_character_like
    channel_id = 568837922288173058
    
    asset_entries = filter_new_asset_entries(
        read_asset_entries(ASSETS_DIRECTORY), get_image_detail_names(TOUHOU_ACTION_ALL),
    )
    registered_action_tags = get_image_detail_tags(TOUHOU_ACTION_ALL)
    
    try:
        for asset_entry in asset_entries:
            message = KOKORO.run(upload(Koishi, asset_entry, channel_id))
            
            attachment = message.attachment
            if attachment is None:
                raise RuntimeError(f'Message created with attachment has no attachment: {message!r}.')
            
            characters, action_tags, unidentified = classify_asset_entry_parts(
                asset_entry, registered_action_tags, get_touhou_character_like
            )
            producer = get_producer_for(characters, action_tags, unidentified)
            url = parse_signed_url(attachment.url).url
            sys.stdout.write(''.join([*producer(characters, action_tags, unidentified, creator, url)]))
    
    finally:
        KOKORO.stop()
