import vampytest

from ..duration_suggestion_set import DurationSuggestionSet


def _assert_fields_set(duration_suggestion_set):
    """
    Asserts whether every fields are set of the given duration suggestion set.
    
    Parameters
    ----------
    duration_suggestion_set : ``DurationSuggestionSet``
    """
    vampytest.assert_instance(duration_suggestion_set, DurationSuggestionSet)
    vampytest.assert_instance(duration_suggestion_set.durations, tuple)
    vampytest.assert_instance(duration_suggestion_set.id, int)


def tets__DurationSuggestionSet__new():
    """
    Tests whether ``DurationSuggestionSet.__new__`` works as intended.
    """
    duration_suggestion_set_id = 9910
    durations = (14400, 15000)
    
    duration_suggestion_set = DurationSuggestionSet(
        duration_suggestion_set_id,
        durations,
    )
    
    _assert_fields_set(duration_suggestion_set)
    
    vampytest.assert_eq(duration_suggestion_set.id, duration_suggestion_set_id)
    vampytest.assert_eq(duration_suggestion_set.durations, durations)


def tets__DurationSuggestionSet__repr():
    """
    Tests whether ``DurationSuggestionSet.__new__`` works as intended.
    """
    duration_suggestion_set_id = 9910
    durations = (14400, 15000)
    
    duration_suggestion_set = DurationSuggestionSet(
        duration_suggestion_set_id,
        durations,
    )
    
    output = repr(duration_suggestion_set)
    vampytest.assert_instance(output, str)
