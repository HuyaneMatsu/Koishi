__all__ = ()


from ..constants import DURATION_SUGGESTION_SETS

from .duration_suggestion_set import DurationSuggestionSet
from .duration_suggestion_set_ids import DURATION_SUGGESTION_SET_ID_MEDIUM, DURATION_SUGGESTION_SET_ID_NEARBY


DURATION_SUGGESTION_SET_NEARBY = \
DURATION_SUGGESTION_SETS[DURATION_SUGGESTION_SET_ID_NEARBY] = DurationSuggestionSet(
    DURATION_SUGGESTION_SET_ID_NEARBY,
    (
        4 * 3600,
        6 * 3600,
        8 * 3600,
        10 * 3600,
        12 * 3600,
        14 * 3600,
        16 * 3600,
    ),
)


DURATION_SUGGESTION_SET_MEDIUM = \
DURATION_SUGGESTION_SETS[DURATION_SUGGESTION_SET_ID_MEDIUM] = DurationSuggestionSet(
    DURATION_SUGGESTION_SET_ID_MEDIUM,
    (
        12 * 3600,
        14 * 3600,
        16 * 3600,
        20 * 3600,
        22 * 3600,
        24 * 3600,
    ),
)
