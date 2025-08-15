__all__ = ()


from ..constants import DURATION_SUGGESTION_SETS

from .duration_suggestion_set import DurationSuggestionSet
from .duration_suggestion_set_ids import DURATION_SUGGESTION_SET_ID_GARDENING


DURATION_SUGGESTION_SET_GARDENING = \
DURATION_SUGGESTION_SETS[DURATION_SUGGESTION_SET_ID_GARDENING] = DurationSuggestionSet(
    DURATION_SUGGESTION_SET_ID_GARDENING,
    (
        4 * 3600,
        6 * 3600,
        8 * 3600,
        10 * 3600,
        12 * 3600,
        14 * 3600,
        16 * 3600,
    )
)
