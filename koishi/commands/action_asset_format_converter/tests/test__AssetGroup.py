import vampytest

from ..asset import Asset
from ..asset_entry import AssetEntry
from ..asset_group import AssetGroup


def _assert_fields_set(asset_group):
    """
    Asserts whether every fields are set of the given asset group.
    
    Parameters
    ----------
    assert_group : ``AssetGroup``
        The assert group to test.
    """
    vampytest.assert_instance(asset_group, AssetGroup)
    vampytest.assert_instance(asset_group.assets, dict, nullable = True)
    vampytest.assert_instance(asset_group.prefix, str)


def test__AssetGroup__new():
    """
    Tests whether ``AssetGroup.__new__`` works as intended.
    """
    prefix = 'murasa'
    
    asset_group = AssetGroup(prefix)
    _assert_fields_set(asset_group)
    
    vampytest.assert_eq(asset_group.prefix, prefix)


def test__AssetGroup__repr():
    """
    Tests whether ``AssetGroup.__new__`` works as intended.
    """
    prefix = 'murasa'
    
    entry_0 = AssetEntry(prefix, 0, None, 'png')
    
    asset_group = AssetGroup(prefix)
    asset_group.add_entry(entry_0)
    
    output = repr(asset_group)
    vampytest.assert_instance(output, str)



def _iter_options__eq():
    prefix = 'murasa'
    extension = 'png'
    keyword_parameters = {
        'prefix': prefix,
    }
    
    variant_0 = 'hey'
    variant_1 = 'mister'
    
    asset_entry_0 = AssetEntry(prefix, 5, variant_0, extension)
    asset_entry_1 = AssetEntry(prefix, 6, variant_1, extension)
    
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
        ],
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
        ],
        True,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
        ],
        {
            **keyword_parameters,
            'prefix': 'kutaka',
        },
        [
            asset_entry_0,
            asset_entry_1,
        ],
        False,
    )
    
    yield (
        keyword_parameters,
        [
            asset_entry_0,
            asset_entry_1,
        ],
        keyword_parameters,
        [
            asset_entry_0,
        ],
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AssetGroup__eq(keyword_parameters_0, asset_entries_0, keyword_parameters_1, asset_entries_1):
    """
    Tests whether ``AssetGroup.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    asset_entries_0 : `list<AssetEntry>`
        Asset entries to add to the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Asset parameters to create instance with.
    
    asset_entries_1 : `list<AssetEntry>`
        AssetGroup entries to add to the instance.
    
    Returns
    -------
    output : `bool`
    """
    asset_0 = AssetGroup(**keyword_parameters_0)
    for asset_entry in asset_entries_0:
        asset_0.add_entry(asset_entry)
    
    asset_1 = AssetGroup(**keyword_parameters_1)
    for asset_entry in asset_entries_1:
        asset_1.add_entry(asset_entry)
    
    output = asset_0 == asset_1
    vampytest.assert_instance(output, bool)
    return output


def test__AssetGroup__add_entry():
    """
    Tests whether ``AssetGroup.add_entry`` works as intended.
    """
    prefix = 'murasa'
    index = 5
    postfix = None
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    
    asset = Asset(index, extension)
    asset.add_variant(asset_entry)
    
    vampytest.assert_eq(asset_group.assets, None)
    
    asset_group.add_entry(asset_entry)
    
    vampytest.assert_eq(asset_group.assets, {(index, extension): asset})
    
    asset_group.add_entry(asset_entry)
    
    vampytest.assert_eq(asset_group.assets, {(index, extension): asset})


def test__AssetGroup__add_entry__varianted():
    """
    Tests whether ``AssetGroup.add_entry`` works as intended.
    
    Case: varianted.
    """
    prefix = 'murasa'
    index = 5
    postfix_0 = None
    postfix_1 = 'mister'
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index, postfix_0, extension)
    asset_entry_1 = AssetEntry(prefix, index, postfix_1, extension)
    
    asset = Asset(index, extension)
    asset.add_variant(asset_entry_0)
    asset.add_variant(asset_entry_1)
    
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    vampytest.assert_eq(asset_group.assets, {(index, extension): asset})


def test__AssetGroup__add_entry__multiple():
    """
    Tests whether ``AssetGroup.add_entry`` works as intended.
    
    Case: multiple.
    """
    prefix = 'murasa'
    index_0 = 5
    index_1 = 6
    postfix = None
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index_0, postfix, extension)
    asset_entry_1 = AssetEntry(prefix, index_1, postfix, extension)
    
    asset_0 = Asset(index_0, extension)
    asset_0.add_variant(asset_entry_0)
    
    asset_1 = Asset(index_1, extension)
    asset_1.add_variant(asset_entry_1)
    
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    vampytest.assert_eq(asset_group.assets, {(index_0, extension): asset_0, (index_1, extension): asset_1})


def test__AssetGroup__pop_first_incorrect_asset__nothing_to_pop():
    """
    Tests whether ``AssetGroup.pop_first_incorrect_asset`` works as intended.
    
    Case: nothing to pop.
    """
    prefix = 'murasa'
    
    asset_group = AssetGroup(prefix)
    
    output = asset_group.pop_first_incorrect_asset()
    vampytest.assert_eq(asset_group.assets, None)
    vampytest.assert_instance(output, Asset, nullable = True)
    vampytest.assert_eq(output, None)


def test__AssetGroup__pop_first_incorrect_asset__no_bad_entries():
    """
    Tests whether ``AssetGroup.pop_first_incorrect_asset`` works as intended.
    
    Case: no bad entries.
    """
    prefix = 'murasa'
    index = 5
    postfix = None
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    asset_group.add_entry(asset_entry)
    
    asset = Asset(index, extension)
    asset.add_variant(asset_entry)
    
    output = asset_group.pop_first_incorrect_asset()
    vampytest.assert_eq(asset_group.assets, {(index, extension): asset})
    vampytest.assert_instance(output, Asset, nullable = True)
    vampytest.assert_eq(output, None)


def test__AssetGroup__pop_first_incorrect_asset__last_bad_entry():
    """
    Tests whether ``AssetGroup.pop_first_incorrect_asset`` works as intended.
    
    Case: no bad entries.
    """
    prefix = 'murasa'
    index = 5
    postfix = None
    extension = 'jpg'
    
    asset_group = AssetGroup(prefix)
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    asset_group.add_entry(asset_entry)
    
    asset = Asset(index, extension)
    asset.add_variant(asset_entry)
    
    output = asset_group.pop_first_incorrect_asset()
    vampytest.assert_eq(asset_group.assets, None)
    vampytest.assert_instance(output, Asset, nullable = True)
    vampytest.assert_eq(output, asset)


def test__AssetGroup__pop_first_incorrect_asset__multiple_entries():
    """
    Tests whether ``AssetGroup.pop_first_incorrect_asset`` works as intended.
    
    Case: multiple entries.
    """
    prefix = 'murasa'
    index = 5
    postfix = None
    extension_0 = 'jpg'
    extension_1 = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index, postfix, extension_0)
    asset_entry_1 = AssetEntry(prefix, index, postfix, extension_1)
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    asset_0 = Asset(index, extension_0)
    asset_0.add_variant(asset_entry_0)
    asset_1 = Asset(index, extension_1)
    asset_1.add_variant(asset_entry_1)
    
    output = asset_group.pop_first_incorrect_asset()
    vampytest.assert_eq(asset_group.assets, {(index, extension_1): asset_1})
    vampytest.assert_instance(output, Asset, nullable = True)
    vampytest.assert_eq(output, asset_0)


def test__AssetGroup__find_best_fit_index__no_assets():
    """
    Tests whether ``AssetGroup.find_best_fit_index`` works as intended.
    
    Case: no assets.
    """
    prefix = 'murasa'
    
    asset_group = AssetGroup(prefix)
    
    output = asset_group.find_best_fit_index()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)


def test__AssetGroup__find_best_fit_index__index_only_higher():
    """
    Tests whether ``AssetGroup.find_best_fit_index`` works as intended.
    
    Case: index only higher.
    """
    prefix = 'murasa'
    index_0 = 5
    index_1 = 4
    postfix = None
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index_0, postfix, extension)
    asset_entry_1 = AssetEntry(prefix, index_1, postfix, extension)
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    output = asset_group.find_best_fit_index()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)


def test__AssetGroup__find_best_fit_index__index_only_lower():
    """
    Tests whether ``AssetGroup.find_best_fit_index`` works as intended.
    
    Case: index only lower.
    """
    prefix = 'murasa'
    index_0 = 0
    index_1 = 1
    postfix = None
    extension = 'png'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index_0, postfix, extension)
    asset_entry_1 = AssetEntry(prefix, index_1, postfix, extension)
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    output = asset_group.find_best_fit_index()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)


def test__AssetGroup__find_best_fit_index__ignore_incorrect_extension():
    """
    Tests whether ``AssetGroup.find_best_fit_index`` works as intended.
    
    Case: ignore incorrect extension.
    """
    prefix = 'murasa'
    index_0 = 0
    index_1 = 1
    postfix = None
    extension = 'jpg'
    
    asset_group = AssetGroup(prefix)
    asset_entry_0 = AssetEntry(prefix, index_0, postfix, extension)
    asset_entry_1 = AssetEntry(prefix, index_1, postfix, extension)
    asset_group.add_entry(asset_entry_0)
    asset_group.add_entry(asset_entry_1)
    
    output = asset_group.find_best_fit_index()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
