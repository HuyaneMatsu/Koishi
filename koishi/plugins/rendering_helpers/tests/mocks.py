from datetime import datetime as DateTime


class DateTimeMock(DateTime):
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, time_zone):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(time_zone)
        return value


def is_instance_mock(instance, accepted_type):
    if isinstance(instance, DateTime) and (accepted_type is DateTimeMock):
        return True
    
    return isinstance(instance, accepted_type)
