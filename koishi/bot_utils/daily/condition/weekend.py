__all__ = ('ConditionWeekend',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs

from .base import ConditionBase


class ConditionWeekend(ConditionBase):
    """
    Condition whether it is weekend.
    """
    __slots__ = ()
    
    @copy_docs(ConditionBase.__call__)
    def __call__(self, user):
        return DateTime.now(TimeZone.utc).weekday() > 4
