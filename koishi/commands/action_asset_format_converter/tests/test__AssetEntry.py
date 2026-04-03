import vampytest

from ..asset_entry import AssetEntry


def _assert_fields_set(asset_entry):
    """
    tests whether every fields are set of the given asset entry.
    
    Parameters
    ----------
    asset_entry : ``AssetEntry``
        The asset entry to check.
    """
    vampytest.assert_instance(asset_entry, AssetEntry)
    vampytest.assert_instance(asset_entry._cache_name, str, nullable = True)
    vampytest.assert_instance(asset_entry.extension, str)
    vampytest.assert_instance(asset_entry.index, int)
    vampytest.assert_instance(asset_entry.prefix, str)
    vampytest.assert_instance(asset_entry.postfix, str, nullable = True)


def test__AssetEntry__new():
    """
    Tests whether ``AssetEntry.__new__`` works as intended.
    """
    prefix = 'kosuzu'
    index = 5
    postfix = 'original'
    extension = 'png'
    
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    _assert_fields_set(asset_entry)
    
    vampytest.assert_eq(asset_entry.prefix, prefix)
    vampytest.assert_eq(asset_entry.index, index)
    vampytest.assert_eq(asset_entry.postfix, postfix)
    vampytest.assert_eq(asset_entry.extension, extension)


def test__AssetEntry__repr():
    """
    Tests whether ``AssetEntry.__repr__`` works as intended.
    """
    prefix = 'kosuzu'
    index = 5
    postfix = 'original'
    extension = 'png'
    
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    
    output = repr(asset_entry)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    prefix = 'kosuzu'
    index = 5
    postfix = 'original'
    extension = 'png'
    
    keyword_parameters = {
        'prefix': prefix,
        'index': index,
        'postfix': postfix,
        'extension': extension,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'prefix': 'akyuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'index': 6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'postfix': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'extension': 'jpg',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AssetEntry__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AssetEntry.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    asset_entry_0 = AssetEntry(**keyword_parameters_0)
    asset_entry_1 = AssetEntry(**keyword_parameters_1)
    
    output = asset_entry_0 == asset_entry_1
    vampytest.assert_instance(output, bool)
    return output


def test__AssetEntry__reconstruct_file_name__no_postfix():
    """
    Tests whether ``AssetEntry.reconstruct_file_name`` works as intended.
    
    Case: No postfix.
    """
    prefix = 'kosuzu'
    index = 5
    postfix = None
    extension = 'png'
    
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    
    output = asset_entry.reconstruct_file_name()
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'kosuzu-0005.png')


def test__AssetEntry__reconstruct_file_name__with_postfix():
    """
    Tests whether ``AssetEntry.reconstruct_file_name`` works as intended.
    
    Case: With postfix.
    """
    prefix = 'kosuzu'
    index = 5
    postfix = 'original'
    extension = 'png'
    
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    
    output = asset_entry.reconstruct_file_name()
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'kosuzu-0005-original.png')


def test__AssetEntry__name():
    """
    Tests whether `AssetEntry.name`` works as intended.
    """
    prefix = 'kosuzu'
    index = 5
    postfix = 'original'
    extension = 'png'
    
    asset_entry = AssetEntry(prefix, index, postfix, extension)
    output = asset_entry.name
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'kosuzu-0005')
    vampytest.assert_eq(asset_entry._cache_name, output)
