__all__ = ()

from datetime import datetime as DateTime

from hata import Embed
from hata.ext.slash import Button, InteractionResponse, Row

from .calendar_events import CALENDAR_EVENTS
from .constants import (
    COLOR_CODE_RESET, BUTTON_BACK_DISABLED, BUTTON_CLOSE, BUTTON_NEXT_DISABLED, DAY_NAMES_SHORT, EMOJI_BACK, EMOJI_NEXT,
    MONTH_MAX, MONTH_MIN, MONTH_NAMES, YEAR_MAX, YEAR_MIN
)
from .filtering import get_events_for_month


def add_month_field(embed, year, month_number):
    """
    Adds a new field to the embed for the given year-month combination.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    year : `int`
        The year's number to use.
    month_number : `int`
        The month's number.
    """
    by_day = get_events_for_month(month_number, CALENDAR_EVENTS)
    month_name = MONTH_NAMES[month_number]
    
    description_parts = []
    description_parts.append('```ansi\n')
    
    by_day_length = len(by_day)
    if by_day_length:
        by_day_index = 0
        
        
        while True:
            day_number, in_day = by_day[by_day_index]
            
            description_parts.append(DAY_NAMES_SHORT[DateTime(year, month_number, day_number).weekday()])
            description_parts.append(' ')
            description_parts.append(format(day_number, '>2'))
            
            description_parts.append(' ')
            
            in_day_length = len(in_day)
            in_day_index = 0
            
            while True:
                event = in_day[in_day_index]
                
                description_parts.append(event.color_code)
                description_parts.append(event.name)
                description_parts.append(COLOR_CODE_RESET)
                
                in_day_index += 1
                if in_day_index == in_day_length:
                    break
                
                description_parts.append(' & ')
                continue
                
            by_day_index += 1
            if by_day_index == by_day_length:
                break
            
            description_parts.append('\n')
            continue
    
    description_parts.append('\n```')
    
    embed.add_field(month_name, ''.join(description_parts), inline = True)


def build_month_embed(year):
    """
    Builds a month embed.
    
    Parameters
    ----------
    year : `int`
        The month's number.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(f'{year} Touhou calendar')
    
    for month_number in range(MONTH_MIN, MONTH_MAX + 1):
        add_month_field(embed, year, month_number)
    
    return embed


def build_year_component(year):
    """
    Builds a year components for the given year.
    
    Parameters
    ----------
    year : `int`
        The year to get the components for.
    
    Returns
    -------
    component : ``Row``
    """
    if year <= YEAR_MIN:
        button_back = BUTTON_BACK_DISABLED
    else:
        year_previous = year - 1
    
        button_back = Button(
            str(year_previous),
            EMOJI_BACK,
            custom_id = f'touhou_calendar.year.{year_previous}',
        )
    
    if year >= YEAR_MAX:
        button_next = BUTTON_NEXT_DISABLED
    else:
        year_next = year + 1
        
        button_next = Button(
            str(year_next),
            EMOJI_NEXT,
            custom_id = f'touhou_calendar.year.{year_next}',
        )
    
    return Row(
        button_back,
        button_next,
        BUTTON_CLOSE,
    )


RESPONSE_CACHE = {}


def get_response_for_year(year):
    """
    Gets the response the given year.
    
    Parameters
    ----------
    year : `int`
        The year to get the response for.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    try:
        response = RESPONSE_CACHE[year]
    except KeyError:
        response = InteractionResponse(
            embed = build_month_embed(year),
            components = build_year_component(year),
        )
        RESPONSE_CACHE[year] = response
    
    return response
