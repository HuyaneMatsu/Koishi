__all__ = ('produce_kilogram', 'produce_kilogram_ratio', 'produce_meter_per_second', 'produce_speed', 'produce_weight',)


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
    kilo_grams, grams = divmod(weight, 1000)
    yield str(kilo_grams)
    yield '.'
    grams_string = str(grams)
    yield '0' * (3 - len(grams_string))
    yield grams_string


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
