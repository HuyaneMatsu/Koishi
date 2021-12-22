__all__ = ()

import re

from ..utils import PARSE_TIMESTAMP_RP

NoneType = type(None)


ENUM_EXPECTED_NAME_PARTS = (
    'type',
    'style',
    'behavior',
    'state',
    'level',
)

ENUM_EXPECTED_INT_MIN_VALUE = 0
ENUM_EXPECTED_INT_MAX_VALUE = 65
ENUM_EXPECTED_STR_MIN_LENGTH = 1
ENUM_EXPECTED_STR_MAX_LENGTH = 128

ENUM_GUESS_CHANCE_MAX = 2

def guess_is_enum(name, value):
    """
    Guesses whether the given value can be an enum.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if isinstance(value, str):
        if (not value.isupper()) and (not value.isupper()):
            return -1
        
        value_length = len(value)
        if (value_length < ENUM_EXPECTED_STR_MIN_LENGTH):
            return -1
        
        if (value_length > ENUM_EXPECTED_STR_MAX_LENGTH):
            return -1
        
        chance = 1
    
    elif isinstance(value, int):
        if (value < ENUM_EXPECTED_INT_MIN_VALUE):
            return -1
        
        if (value > ENUM_EXPECTED_INT_MAX_VALUE):
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in ENUM_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


AVATAR_RP = re.compile('(?:a_)?[0-9a-f]{32}')

ICON_EXPECTED_NAME_PARTS = (
    'icon',
    'avatar',
    'banner',
    'splash',
)

ICON_GUESS_CHANCE_MAX = 2

def guess_is_icon(name, value):
    """
    Guesses whether the given value is an icon.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Icons default to `0`
        chance = 0
    
    elif isinstance(value, str):
        if value:
            if (AVATAR_RP.fullmatch(value) is None):
                return -1
            
            chance = 1
        else:
            # Deprecated icon strings might be set as empty value.
            chance = 0
        
    else:
        return -1
    
    for expected_name_part in ICON_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


COLOR_EXPECTED_NAME_PARTS = (
    'color',
)

COLOR_EXPECTED_MIN_VALUE = 0x000000
COLOR_EXPECTED_MAX_VALUE = 0xffffff

COLOR_GUESS_MAX_CHANCE = 2

def guess_is_color(name, value):
    """
    Guesses whether the given value is a color.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Colors might default to `None` at cases
        chance = 0
    
    elif isinstance(value, int):
        if value < COLOR_EXPECTED_MIN_VALUE:
            return -1
        
        if value > COLOR_EXPECTED_MAX_VALUE:
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in COLOR_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


SNOWFLAKE_EXPECTED_NAME_PARTS = (
    'id',
)

SNOWFLAKE_EXPECTED_STRING_MIN_VALUE = 1<<21
SNOWFLAKE_EXPECTED_STRING_MAX_VALUE = (1<<64)-1

SNOWFLAKE_EXPECTED_INT_MIN_VALUE = 0
SNOWFLAKE_EXPECTED_INT_MAX_VALUE = (1<<64)-1

SNOWFLAKE_GUESS_MAX_CHANCE = 3


def guess_is_snowflake(name, value):
    """
    Guesses whether the given value is a snowflake.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Snowflake can be `None` at cases. The wrapper uses `0` at these cases
        chance = 0
    
    elif isinstance(value, str):
        if not value.isdecimal():
            return -1
        
        value = int(value)
        if value < SNOWFLAKE_EXPECTED_STRING_MIN_VALUE:
            return -1
        
        if value > SNOWFLAKE_EXPECTED_STRING_MAX_VALUE:
            return -1
        
        chance = 2
    
    elif isinstance(value, int):
        if value < SNOWFLAKE_EXPECTED_INT_MIN_VALUE:
            return -1
        
        if value > SNOWFLAKE_EXPECTED_INT_MAX_VALUE:
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in SNOWFLAKE_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


STRING_EXPECTED_NAME_PARTS = (
    'description',
    'label',
    'name',
    'value',
    'text',
    'default',
    'placeholder',
)

STRING_GUESS_MAX_CHANCE = 2

def guess_is_string_field(name, value):
    """
    Guesses whether the given value is a string field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, str):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in STRING_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


INT_EXPECTED_NAME_PARTS = (
    'value',
    'max',
    'min',
    'length',
)

INT_GUESS_MAX_CHANCE = 2

def guess_is_int_field(name, value):
    """
    Guesses whether the given value is an int field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, int):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in INT_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


FLOAT_EXPECTED_NAME_PARTS = (
    'value',
    'max',
    'min',
)

FLOAT_GUESS_MAX_CHANCE = 2

def guess_is_float_field(name, value):
    """
    Guesses whether the given value is a float field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, float):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in FLOAT_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


TIMESTAMP_EXPECTED_NAME_PARTS = (
    'timestamp',
    '_at',
)

TIMESTAMP_GUESS_MAX_CHANCE = 2

def guess_is_timestamp_field(name, value):
    """
    Guesses whether the given value is a timestamp field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, str):
        if (PARSE_TIMESTAMP_RP.fullmatch(value) is None):
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in TIMESTAMP_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


UNIX_TIME_EXPECTED_NAME_PARTS = (
    'start',
    'end',
)

UNIX_TIME_GUESS_MAX_CHANCE = 2

def guess_is_unix_time(name, value):
    """
    Guesses whether the given value is a timestamp field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, int):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in UNIX_TIME_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


MULTI_TYPE_VALUE_NAME_PARTS = (
    'value',
)

MULTI_TYPE_VALUE_GUESS_MAX_CHANCE = 2

def guess_is_multi_type_value(name, value):
    """
    Guesses whether the given value is a multi type value field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, (int, bool, float, str)):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in MULTI_TYPE_VALUE_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


OBJECT_GUESS_MAX_CHANCE = 1

def guess_is_object(name, value):
    """
    Guesses whether the given value is an object field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, dict):
        chance = 1
    
    else:
        return -1
    
    # No name check
    return chance


ARRAY_GUESS_MAX_CHANCE = 1

def guess_is_array(name, value):
    """
    Guesses whether the given value is an array field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, list):
        chance = 1
    
    else:
        return -1
    
    # No name check
    return chance


GUESSERS = []

class Guesser:
    """
    Raw type guesser, I guess.
    
    Attributes
    ----------
    guesser_function : `FunctionType`
        The guesser.
    guess_max_chance : `int`
        The maximal chance to be returned by the guesser function.
    name : `str`
        The guesser's name.
    sub_node_type : `type`
        Node type for if applicable.
    """
    __slots__ = ('guesser_function', 'guess_max_chance', 'name', 'sub_node_type',)
    
    def __new__(cls, name, guesser_function, guess_max_chance, sub_node_type):
        """
        Creates a new guesser instance.
        
        Parameters
        ----------
        name : `str`
            The guesser's name.
        guesser_function : `FunctionType`
            The guesser.
        guess_max_chance : `int`
            The maximal chance to be returned by the guesser function.
        sub_node_type : `type`
            Node type for if applicable.
        """
        self = object.__new__(cls)
        self.name = name
        self.guesser_function = guesser_function
        self.guess_max_chance = guess_max_chance
        self.sub_node_type = sub_node_type
        
        GUESSERS.append(self)
        
        return self
    
    
    def __repr__(self):
        """Returns the guesser's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        sub_node_type = self.sub_node_type
        if (sub_node_type is not None):
            repr_parts.append(', sub_node_type=')
            repr_parts.append(repr(sub_node_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


class GuessStateNode:
    """
    total_guess_chance : `int`
    
    node : ``GuessNode``
        Guess node if applicable.
    """
    __slots__ = ('node', 'total_guess_chance', )
    
    # todo

class GuesserState:
    """
    Attributes
    ----------
    guessers : `dict` of (``Guesser``, `GuessStateNode`) items
        Then ot yet failed guessers.
    name : `str`
        The node's state.
    received_count : `int`
        The total amount of received values passed to this node.
    received_values : `None` or `dict` of (`object`, `Any`) items
        The already received values.
    """
    __slots__ = ('guessers', 'name', 'received_count', 'received_values')
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        self.received_values = None
        self.guessers = {guesser: GuessStateNode() for guesser in GUESSERS}
        self.received_count = 0
        return self
    
    
    def guess(self, name, value):
        guessers_to_remove = None
        
        guessers = self.guessers
        for guesser, guess_state_node in guessers.items():
            chance = guesser.guesser_function(name, value)
            if chance == -1:
                if guessers_to_remove:
                    guessers_to_remove = []
                
                guessers_to_remove.append(guesser)
            
            else:
                guess_state_node.feed(name, value, chance)
        
        if (guessers_to_remove is not None):
            for guesser in guessers_to_remove:
                del guessers_to_remove[guesser]
        
        
        # todo
