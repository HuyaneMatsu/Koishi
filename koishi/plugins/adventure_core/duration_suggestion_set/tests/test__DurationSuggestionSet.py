import vampytest

from ..duration_suggestion_set import DurationSuggestionSet, duration_suggestion_set_create


def test__duration_suggestion_set_create():
    duration_suggestion_set_id = 9910
    durations = (14400, 15000)
    
    duration_suggestion_set = duration_suggestion_set_create(
        duration_suggestion_set_id,
        durations,
    )
    
    vampytest.assert_instance(duration_suggestion_set, DurationSuggestionSet)
    vampytest.assert_instance(duration_suggestion_set.durations, tuple)
    vampytest.assert_instance(duration_suggestion_set.id, int)
    
    vampytest.assert_eq(duration_suggestion_set.id, duration_suggestion_set_id)
    vampytest.assert_eq(duration_suggestion_set.durations, durations)
