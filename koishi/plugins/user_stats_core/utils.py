__all__ = ('produce_speed', )


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
