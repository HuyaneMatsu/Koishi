__all__ = (
    'produce_duration', 'produce_duration_sophisticated', 'produce_kilogram', 'produce_kilogram_ratio',
    'produce_meter_per_second', 'produce_speed', 'produce_weight',
)


def produce_weight(weight):
    """
    Produces the given weight.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    Yields
    ------
    part : `str`
    """
    while True:
        kilo_grams, grams = divmod(weight, 1000)
        yield str(kilo_grams)
        
        if not grams:
            break
        
        yield '.'
        split, grams = divmod(grams, 100)
        yield str(split)
        
        if not grams:
            break
        
        split, grams = divmod(grams, 10)
        yield str(split)
        
        if not grams:
            break
        
        yield str(grams)
        break


def produce_kilogram(weight):
    """
    Produces a kilogram value.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    weight : `int`
        Weight to produce as kilogram in grams.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_weight(weight)
    yield ' kg'


def produce_kilogram_ratio(weight_0, weight_1):
    """
    Produces a kilogram ratio.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    weight_0 : `int`
        Used weight
    
    weight_1 : `int`
        Total weight.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_weight(weight_0)
    yield ' / '
    yield from produce_weight(weight_1)
    yield ' kg'


def produce_speed(speed):
    """
    Produces the given speed.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    speed : `int`
        Speed in millimeters.
    
    Yields
    ------
    part : `str`
    """
    meters, millimeters = divmod(speed, 1000)
    
    first_decimal, secondary_decimals = divmod(millimeters, 100)
    if secondary_decimals >= 50:
        if first_decimal == 9:
            meters += 1
            first_decimal = 0
        else:
            first_decimal += 1
    
    yield str(meters)
    yield '.'
    yield str(first_decimal)


def produce_meter_per_second(speed):
    """
    Produces the given speed.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    speed : `int`
        Speed in millimeters.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_speed(speed)
    yield ' m/s'


def produce_duration(duration):
    """
    Produces a duration string.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `int`
        Duration to produce.
    
    Yields
    ------
    part : `str`
    """
    element_added = False
    
    while True:
        if not duration:
            break
        
        weeks, duration = divmod(duration, 604800)
        if weeks:
            element_added = True
            
            yield str(weeks)
            yield 'w'
            
            if not duration:
                break
        
        days, duration = divmod(duration, 86400)
        if days:
            if element_added:
                yield ' '
            else:
                element_added = True
            
            yield str(days)
            yield 'd'
            
            if not duration:
                break
        
        hours, duration = divmod(duration, 3600)
        if hours:
            if element_added:
                yield ' '
            else:
                element_added = True
            
            yield str(hours)
            yield 'h'
            
            if not duration:
                break
        
        minutes, duration = divmod(duration, 60)
        if minutes:
            if element_added:
                yield ' '
            else:
                element_added = True
            
            yield str(minutes)
            yield 'm'
            
            if not duration:
                break
        
        break
    
    if duration or (not element_added):
        if element_added:
            yield ' '
        
        yield str(duration)
        yield 's'


def produce_duration_sophisticated(duration):
    """
    Produces a more sophisticated duration string. ``parse_duration`` does not work on the output.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `int`
        Duration to produce.
    
    Yields
    ------
    part : `str`
    """
    element_added = False
    
    while True:
        if not duration:
            break
        
        weeks, duration = divmod(duration, 604800)
        if weeks:
            element_added = True
            
            yield str(weeks)
            yield ' '
            yield ('week' if weeks == 1 else 'weeks')
            
            if not duration:
                break
        
        days, duration = divmod(duration, 86400)
        if days:
            if element_added:
                yield ', '
            else:
                element_added = True
            
            yield str(days)
            yield ' '
            yield ('day' if days == 1 else 'days')
            
            if not duration:
                break
        
        hours, duration = divmod(duration, 3600)
        if hours:
            if element_added:
                yield ', '
            else:
                element_added = True
            
            yield str(hours)
            yield ' '
            yield ('hour' if hours == 1 else 'hours')
            
            if not duration:
                break
        
        minutes, duration = divmod(duration, 60)
        if minutes:
            if element_added:
                yield ', '
            else:
                element_added = True
            
            yield str(minutes)
            yield ' '
            yield ('minute' if minutes == 1 else 'minutes')
            
            if not duration:
                break
        
        break
    
    if duration or (not element_added):
        if element_added:
            yield ', '
        
        yield str(duration)
        yield ' '
        yield ('second' if duration <= 1 else 'seconds')
