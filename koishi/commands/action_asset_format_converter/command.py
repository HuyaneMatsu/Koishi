__all__ = ()

from hata.main import register

from .constants import ASSETS_DIRECTORY
from .grouping import convert_assets, group_assets, read_asset_entries


@register
def convert_action_asset_formats():
    """
    Converts all action command image's format to png as applicable.
    """
    convert_assets(ASSETS_DIRECTORY, group_assets(read_asset_entries(ASSETS_DIRECTORY)))
