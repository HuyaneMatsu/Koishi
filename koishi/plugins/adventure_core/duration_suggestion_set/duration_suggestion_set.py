__all__ = ('DurationSuggestionSet', 'duration_suggestion_set_create')

from scarletio import RichType


class DurationSuggestionSet(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents a duration suggestion set.
    
    Attributes
    ----------
    durations : `tuple<int>`
        The suggested durations.
    
    id : `int`
        The identifier of the duration suggestion set.
    """
    __slots__ = ('durations', 'id')


def duration_suggestion_set_create(duration_suggestion_set_id, durations):
    """
    Creates a new duration suggestion set.
    
    Parameters
    ----------
    duration_suggestion_set_id : `int`
        The identifier of the target.
    
    durations : `tuple<int>`
        The suggested durations.
    
    Returns
    -------
    duration_suggestion_set : ``DurationSuggestionSet``
    """
    duration_suggestion_set = object.__new__(DurationSuggestionSet)
    duration_suggestion_set.durations = durations
    duration_suggestion_set.id = duration_suggestion_set_id
    return duration_suggestion_set
