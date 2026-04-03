__all__ = ()


def sort_key_calendar_event_name(calendar_event):
    """
    Sort key used to sort calendar events by name.
    
    Parameters
    ----------
    calendar_event : ``CalendarEvent``
        The calendar event to get its sort key oof.
    
    Returns
    -------
    sort_key : `str`
    """
    return calendar_event.name


def get_events_for_month(month_number, filter_from):
    """
    Gets the events for the given month sorted by day.
    
    Parameters
    ----------
    month_number : `int`
        The month's number to filter for.
    filter_from : `iterable`
        The events to filter from.
    
    Returns
    -------
    events : `list` of `tuple` (`int`, `list` of ``CalendarEvent``)
    """
    events_in_month = {}
    
    for calendar_event in filter_from:
        if calendar_event.month == month_number:
            try:
                by_day = events_in_month[calendar_event.day]
            except KeyError:
                by_day = []
                events_in_month[calendar_event.day] = by_day
            
            by_day.append(calendar_event)
    
    for by_day in events_in_month.values():
        by_day.sort(key = sort_key_calendar_event_name)
    
    return sorted(events_in_month.items())
