import vampytest

from ..stage_result import StageResult


def _assert_fields_set(stage_result):
    """
    Asserts whether the given stage result has all of its fields set.
    
    Parameters
    ----------
    stage_result : ``StageResult``
        The stage result to check.
    """
    vampytest.assert_instance(stage_result, StageResult)
    vampytest.assert_instance(stage_result.best, int)
    vampytest.assert_instance(stage_result.entry_id, int)
    vampytest.assert_instance(stage_result.stage_id, int)


def test__StageResult__new():
    """
    Tests whether ``StageResult.__new__`` works as intended.
    """
    entry_id = 999
    stage_id = 998
    best = 50
    
    stage_result = StageResult(
        entry_id,
        stage_id,
        best,
    )
    _assert_fields_set(stage_result)
    
    vampytest.assert_eq(stage_result.entry_id, entry_id)
    vampytest.assert_eq(stage_result.stage_id, stage_id)
    vampytest.assert_eq(stage_result.best, best)


def test__StageResult__from_entry():
    """
    Tests whether ``StageResult.from_entry`` works as intended.
    """
    entry_id = 999
    stage_id = 998
    best = 50
    
    entry = {
        'id': entry_id,
        'stage_id': stage_id,
        'best': best,
    }
    
    stage_result = StageResult.from_entry(entry)
    _assert_fields_set(stage_result)
    
    vampytest.assert_eq(stage_result.entry_id, entry_id)
    vampytest.assert_eq(stage_result.stage_id, stage_id)
    vampytest.assert_eq(stage_result.best, best)


def test__StageResult__repr():
    """
    Tests whether ``StageResult.__repr__`` works as intended.
    """
    entry_id = 999
    stage_id = 998
    best = 50
    
    stage_result = StageResult(
        entry_id,
        stage_id,
        best,
    )
    
    output = repr(stage_result)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    entry_id = 999
    stage_id = 998
    best = 50
    
    keyword_parameters = {
        'entry_id': entry_id,
        'stage_id': stage_id,
        'best': best,
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
            'entry_id': 800, 
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'stage_id': 801, 
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'best': 51, 
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__StageResult__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``StageResult.__eq__`` works as intended.
    
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
    stage_result_0 = StageResult(**keyword_parameters_0)
    stage_result_1 = StageResult(**keyword_parameters_1)
    
    output = stage_result_0 == stage_result_1
    vampytest.assert_instance(output, bool)
    return output
