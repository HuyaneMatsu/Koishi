from datetime import datetime as DateTime


class DateTimeMock(DateTime):
    __slots__ = ()
    current_date_time = None
    
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    
    @classmethod
    def now(cls, tz):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(tz)
        return value
