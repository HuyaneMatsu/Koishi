import vampytest

from ..asset import Asset
from ..asset_entry import AssetEntry


def _assert_fields_set(asset):
    """
    Tests whether the asset has all of its fields set.
    
    Parameters
    ----------
    asset : ``Asset``
        The asset to check.
    """
    vampytest.assert_instance(asset, Asset)
    vampytest.assert_instance(asset.default_variant, bool)
    vampytest.assert_instance(asset.extension, str)
    vampytest.assert_instance(asset.index, int)
    vampytest.assert_instance(asset.variants, list, nullable = True)


def test__Asset__new():
    """
    Tests whether ``Asset.__new__`` works as intended.
    """
    index = 5
    extension = 'png'
    
    asset = Asset(index, extension)
    _assert_fields_set(asset)
    
    vampytest.assert_eq(asset.index, index)
    vampytest.assert_eq(asset.extension, extension)


def test__Asset__repr():
    """
    Tests whether ``Asset.__repr__`` works as intended.
    """
    index = 5
    extension = 'png'
    
    asset = Asset(index, extension)
    
    output = repr(asset)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    index = 5
    extension = 'png'
    keyword_parameters = {
        'index': index,
        'extension': extension,
    }
    
    variant_0 = 'hey'
    variant_1 = 'mister'
    
    asset_entry_0 = AssetEntry('', index, None, extension)
    asset_entry_1 = AssetEntry('', index, variant_0, extension)
    asset_entry_2 = AssetEntry('', index, variant_1, extension)
    
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        True,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        {
            **keyword_parameters,
            'index': 6,
        },
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        False,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        {
            **keyword_parameters,
            'extension': 'jpg',
        },
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        False,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        keyword_parameters,
        [
            asset_entry_1,
            asset_entry_2,
        ],
        False,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
        ],
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_2,
        ],
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Asset__eq(keyword_parameters_0, asset_entries_0, keyword_parameters_1, asset_entries_1):
    """
    Tests whether ``Asset.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    asset_entries_0 : `list<AssetEntry>`
        Asset entries to add variants the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    asset_entries_1 : `list<AssetEntry>`
        Asset entries to add variants the instance.
    
    Returns
    -------
    output : `bool`
    """
    asset_0 = Asset(**keyword_parameters_0)
    for asset_entry in asset_entries_0:
        asset_0.add_variant(asset_entry)
    
    asset_1 = Asset(**keyword_parameters_1)
    for asset_entry in asset_entries_1:
        asset_1.add_variant(asset_entry)
    
    output = asset_0 == asset_1
    vampytest.assert_instance(output, bool)
    return output


def test__Asset__add_variant__default():
    """
    Tests whether ``Asset.add_variant`` works as intended.
    
    Case: default.
    """
    index = 5
    extension = 'png'
    
    asset = Asset(index, extension)
    vampytest.assert_eq(asset.default_variant, False)
    vampytest.assert_is(asset.variants, None)
    
    asset_entry = AssetEntry('', index, None, extension)
    
    asset.add_variant(asset_entry)
    vampytest.assert_eq(asset.default_variant, True)
    vampytest.assert_is(asset.variants, None)
    
    # Check second try + same
    asset.add_variant(asset_entry)
    vampytest.assert_eq(asset.default_variant, True)
    vampytest.assert_is(asset.variants, None)


def test__Asset__add_variant__custom():
    """
    Tests whether ``Asset.add_variant`` works as intended.
    
    Case: custom.
    """
    index = 5
    extension = 'png'
    variant_0 = 'hey'
    variant_1 = 'mister'
    
    asset = Asset(index, extension)
    vampytest.assert_eq(asset.default_variant, False)
    vampytest.assert_is(asset.variants, None)
    
    asset_entry_0 = AssetEntry('', index, variant_0, extension)
    asset_entry_1 = AssetEntry('', index, variant_1, extension)
    
    asset.add_variant(asset_entry_1)
    vampytest.assert_eq(asset.default_variant, False)
    vampytest.assert_eq(asset.variants, ['mister'])
    
    # Check second try + sorting
    asset.add_variant(asset_entry_0)
    vampytest.assert_eq(asset.default_variant, False)
    vampytest.assert_eq(asset.variants, ['hey', 'mister'])
    
    # Check second try + same
    asset.add_variant(asset_entry_0)
    vampytest.assert_eq(asset.default_variant, False)
    vampytest.assert_eq(asset.variants, ['hey', 'mister'])


def test__Asset__iter_postfix_variants__empty():
    """
    Tests whether ``Asset.iter_postfix_variants`` works as intended.
    
    Case: empty.
    """
    index = 5
    extension = 'png'
    
    asset = Asset(index, extension)
    
    vampytest.assert_eq(
        [*asset.iter_postfix_variants()],
        [],
    )


def test__Asset__iter_postfix_variants__full():
    """
    Tests whether ``Asset.iter_postfix_variants`` works as intended.
    
    Case: full.
    """
    index = 5
    extension = 'png'
    variant_0 = 'hey'
    variant_1 = 'mister'
    
    asset = Asset(index, extension)
    
    asset_entry_0 = AssetEntry('', index, None, extension)
    asset_entry_1 = AssetEntry('', index, variant_0, extension)
    asset_entry_2 = AssetEntry('', index, variant_1, extension)
    
    asset.add_variant(asset_entry_0)
    asset.add_variant(asset_entry_1)
    asset.add_variant(asset_entry_2)
    
    vampytest.assert_eq(
        [*asset.iter_postfix_variants()],
        [None, 'hey', 'mister'],
    )
