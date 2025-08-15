__all__ = ('RETURNS_ALLOWED',)

from ..constants import RETURNS

from .return_ import Return
from .return_ids import RETURN_ID_AFTER, RETURN_ID_BEFORE


RETURN_BEFORE = RETURNS[RETURN_ID_BEFORE] = Return(
    RETURN_ID_BEFORE,
    'Before',
)

RETURN_AFTER = RETURNS[RETURN_ID_AFTER] = Return(
    RETURN_ID_AFTER,
    'After',
)

RETURNS_ALLOWED = (
    RETURN_BEFORE,
    RETURN_AFTER,
)
