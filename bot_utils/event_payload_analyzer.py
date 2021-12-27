__all__ = ()

import re, reprlib
from math import floor

from scarletio import copy_docs, RichAttributeErrorBaseType
from hata.discord.utils import PARSE_TIMESTAMP_RP

NoneType = type(None)

INDENT = '   '
UNKNOWN_FIELD_TYPE_NAME = 'unknown'
GUESS_CHANCE_MULTIPLIER_BY_PARENT = 0.25


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
    if value is None:
        # At some weird cases `value` can be `None` even at the case of enums.
        chance = 0
    
    elif isinstance(value, str):
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


DISCRIMINATOR_EXPECTED_NAME_PARTS = (
    'discriminator',
)

DISCRIMINATOR_EXPECTED_LENGTH = 4

DISCRIMINATOR_GUESS_MAX_CHANCE = 2


def guess_is_discriminator(name, value):
    """
    Guesses whether the given value is a discriminator.
    
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
        # discriminator cannot be `None`.
        return -1
    
    elif isinstance(value, str):
        if len(value) != DISCRIMINATOR_EXPECTED_LENGTH:
            return -1
        
        if not value.isdecimal():
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in DISCRIMINATOR_EXPECTED_NAME_PARTS:
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
    '_until',
)

TIMESTAMP_GUESS_MAX_CHANCE = 2

def guess_is_timestamp(name, value):
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

def collect_guessers_recursively(collected_guessers, guessers):
    """
    Collects guessers recursively.
    
    Parameters
    ----------
    collected_guessers : `None` or `set` of ``Guesser``
        The already collected guessers.
    guessers : `None` or `iterable` of ``Guesser``
        The guessers to collect from.
    
    Returns
    -------
    collected_guessers : `None` or `set` of ``Guesser``
        The collected guessers.
    """
    if (guessers is not None):
        for guesser in guessers:
            if collected_guessers is None:
                collected_guessers = set()
            else:
                if guesser in collected_guessers:
                    continue
            
            collected_guessers.add(guesser)
            collected_guessers = collect_guessers_recursively(collected_guessers, guesser.parents)
    
    return collected_guessers


class Guesser(RichAttributeErrorBaseType):
    """
    Raw type guesser, I guess.
    
    Attributes
    ----------
    collect_values : `bool`
        Whether values should be collected or nah.
    guesser_function : `FunctionType`
        The guesser.
    guess_max_chance : `int`
        The maximal chance to be returned by the guesser function.
    name : `str`
        The guesser's name.
    render_all_values : `bool`
        Whether values should be rendered when the field is displayed.
    sub_node_type : `type`
        Node type for if applicable.
    parents : `None` or `set` of ``Guesser``
        Parent guessers.
    """
    __slots__ = ('collect_values', 'guess_max_chance', 'guesser_function', 'name', 'parents', 'render_all_values',
        'sub_node_type')
    
    def __new__(cls, guesser_function, guess_max_chance, name, sub_node_type, collect_values, render_all_values,
            parents):
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
        collect_values : `bool`
            Whether values should be collected or nah.
        render_all_values : `bool`
            Whether values should be rendered when the field is displayed.
        parents : `None` or `iterable` of ``Guesser``
            Parent guessers.
        """
        parents = collect_guessers_recursively(None, parents)
        
        self = object.__new__(cls)
        self.name = name
        self.guesser_function = guesser_function
        self.guess_max_chance = guess_max_chance
        self.sub_node_type = sub_node_type
        self.collect_values = collect_values
        self.render_all_values = render_all_values
        self.parents = parents
        
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

# Define sub-nodes

class SubNodeBase(RichAttributeErrorBaseType):
    """
    Base class for sub nodes.
    
    Attributes
    ----------
    name : `str`
        The name of the sub-node.
    """
    __slots__ = ('name', )
    
    def __new__(cls, name):
        """
        Creates a new sub node.
        
        Parameters
        ----------
        name : `str`
            The name of the sub-node.
        """
        self = object.__new__(cls)
        self.name = name
        return self
    
    
    def feed(self, value):
        """
        Feeds a value to the node.
        
        Parameters
        ----------
        value : `Any`
            The fed value.
        """
        pass
    
    
    def render_into(self, into, indent):
        """
        Renders the sub-node to the given list.
        
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        """
        pass


class ArraySubNode(SubNodeBase):
    """
    Attributes
    ----------
    name : `str`
        The name of the array.
        
        This name is applied to the names of the elements.
    
    nullable : `bool`
        Whether the field is nullable.
    min_length : `int`
        The minimal length of array received.
    max_length : `int`
        The maximal length of array received.
    state : ``GuesserState``
        Guesser state for the elements for the sub-nodes.
    """
    __slots__ = ('state', 'nullable', 'min_length', 'max_length')
    
    @copy_docs(SubNodeBase.__new__)
    def __new__(cls, name):
        self = SubNodeBase.__new__(cls, name)
        self.state = GuesserState(name)
        self.nullable = False
        self.min_length = -1
        self.max_length = -1
        return self
    
    
    @copy_docs(SubNodeBase.feed)
    def feed(self, value):
        if (value is None):
            self.nullable = True
        else:
            length = len(value)
            
            min_length = self.min_length
            if (min_length == -1) or (length < min_length):
                self.min_length = length
            
            max_length = self.max_length
            if (max_length == -1) or (length > max_length):
                self.max_length = length
            
            for element in value:
                self.state.feed(element)
        
    
    @copy_docs(SubNodeBase.render_into)
    def render_into(self, into, indent):
        
        into.append(' of ')
        
        self.state.render_into(into, indent+1, True)
        
        nullable = self.nullable
        min_length = self.min_length
        max_length = self.max_length
        if nullable or (min_length != -1) or (max_length != -1):
            
            into.append('\n')
            
            for counter in range(indent+1):
                into.append(INDENT)
            
            into.append('details:')
            
            if nullable:
                
                into.append('\n')
                for counter in range(indent+2):
                    into.append(INDENT)
                
                into.append('nullable: true')
            
            if (min_length != -1) and (max_length != -1) and (min_length == max_length):
                    into.append('\n')
                    for counter in range(indent+2):
                        into.append(INDENT)
                    
                    into.append('length: ')
                    into.append(repr(min_length))
            
            else:
                if (min_length != -1):
                    
                    into.append('\n')
                    for counter in range(indent+2):
                        into.append(INDENT)
                    
                    into.append('min_length: ')
                    into.append(repr(min_length))
                
                if (max_length != -1):
                    
                    into.append('\n')
                    for counter in range(indent+2):
                        into.append(INDENT)
                    
                    into.append('max_length: ')
                    into.append(repr(max_length))
        
        self.state.render_most_commons_into(into, indent)


class ObjectSubNode(SubNodeBase):
    """
    Attributes
    ----------
    name : `str`
        The name of the array.
        
        This name is applied to the names of the elements.
    
    state : `dict` of (`str`, ``GuesserState``) items
        Guesser state for the elements for the sub-nodes.
    """
    __slots__ = ('states',)
    
    @copy_docs(SubNodeBase.__new__)
    def __new__(cls, name):
        self = SubNodeBase.__new__(cls, name)
        self.states = {}
        return self
    
    
    @copy_docs(SubNodeBase.feed)
    def feed(self, value):
        if (value is not None):
            for name, element in value.items():
                try:
                    state = self.states[name]
                except KeyError:
                    state = GuesserState(name)
                    self.states[name] = state
                
                state.feed(element)
    
    
    @copy_docs(SubNodeBase.render_into)
    def render_into(self, into, indent):
        into.append('\n')
        
        for counter in range(indent):
            into.append(INDENT)
        
        into.append('{')
        
        states = self.states
        if states:
            into.append('\n')
            
            for state in states.values():
                state.render_into(into, indent+1, False)
                into.append('\n')
        
        for counter in range(indent):
            into.append(INDENT)
        
        into.append('}')


# Define guessers


MULTI_TYPE_GUESSER = Guesser(
    guess_is_multi_type_value,
    MULTI_TYPE_VALUE_GUESS_MAX_CHANCE,
    'multi_type',
    None,
    True,
    False,
    None,
)

STRING_GUESSER = Guesser(
    guess_is_string_field,
    STRING_GUESS_MAX_CHANCE,
    'string',
    None,
    True,
    False,
    (
        MULTI_TYPE_GUESSER,
    ),
)


INT_GUESSER = Guesser(
    guess_is_int_field,
    INT_GUESS_MAX_CHANCE,
    'int',
    None,
    True,
    False,
    (
        MULTI_TYPE_GUESSER,
    ),
)


FLOAT_GUESSER = Guesser(
    guess_is_float_field,
    FLOAT_GUESS_MAX_CHANCE,
    'float',
    None,
    True,
    False,
    (
        MULTI_TYPE_GUESSER,
    ),
)

ENUM_GUESSER = Guesser(
    guess_is_enum,
    ENUM_GUESS_CHANCE_MAX,
    'enum',
    None,
    True,
    True,
    (
        INT_GUESSER,
        STRING_GUESSER,
    ),
)


ICON_GUESSER = Guesser(
    guess_is_icon,
    ICON_GUESS_CHANCE_MAX,
    'icon',
    None,
    True,
    False,
    (
        STRING_GUESSER,
    ),
)


COLOR_GUESSER = Guesser(
    guess_is_color,
    COLOR_GUESS_MAX_CHANCE,
    'color',
    None,
    True,
    False,
    (
        INT_GUESSER,
    ),
)


SNOWFLAKE_GUESSER = Guesser(
    guess_is_snowflake,
    SNOWFLAKE_GUESS_MAX_CHANCE,
    'snowflake',
    None,
    True,
    False,
    (
        INT_GUESSER,
        STRING_GUESSER,
    ),
)


TIMESTAMP_GUESSER = Guesser(
    guess_is_timestamp,
    TIMESTAMP_GUESS_MAX_CHANCE,
    'timestamp',
    None,
    True,
    False,
    (
        STRING_GUESSER,
    ),
)


UNIX_TIME_GUESSER = Guesser(
    guess_is_unix_time,
    UNIX_TIME_GUESS_MAX_CHANCE,
    'unix_time',
    None,
    True,
    False,
    (
        INT_GUESSER,
    ),
)


OBJECT_GUESSER = Guesser(
    guess_is_object,
    OBJECT_GUESS_MAX_CHANCE,
    'object',
    ObjectSubNode,
    False,
    False,
    None,
)

ARRAY_GUESSER = Guesser(
    guess_is_array,
    ARRAY_GUESS_MAX_CHANCE,
    'array',
    ArraySubNode,
    False,
    False,
    None,
)

DISCRIMINATOR_GUESSER = Guesser(
    guess_is_discriminator,
    DISCRIMINATOR_GUESS_MAX_CHANCE,
    'discriminator',
    None,
    True,
    False,
    (
        STRING_GUESSER,
    ),
)


def freeze(value):
    """
    Freezes the given object.
    
    Parameters
    ----------
    value : `object`
        The value to freeze.
    
    Returns
    -------
    value : `object`
        The frozen value.
    """
    if (value is None):
        pass
    elif isinstance(value, (str, int, float)):
        pass
    elif isinstance(value, list):
        value = tuple(freeze(element) for element in value)
    elif isinstance(value, dict):
        value = FrozenDict(value)
    else:
        pass
    
    return value


class FrozenDict(RichAttributeErrorBaseType):
    """
    Represents a hashable dictionary.
    
    Attributes
    ----------
    hash_value : `int`
        The hashed value of the dictionary.
    value : `dict`
        The frozen dictionary.
    """
    __slots__ = ('hash_value', 'value')
    
    def __new__(cls, source_dictionary):
        """
        Creates a new frozen dict from the given non-frozen one.
        
        Parameters
        ----------
        source_dictionary : `dict`
        """
        frozen_dictionary = {key: freeze(value) for key, value in source_dictionary.items()}
        
        # Let python do the work for us.
        hash_value = hash(tuple(frozen_dictionary.items()))
        
        self = object.__new__(cls)
        self.value = source_dictionary
        self.hash_value = hash_value
        return self
    
    def __hash__(self):
        """Returns the hash value of the frozen dictionary."""
        return self.hash_value
    
    def __eq__(self, other):
        """Returns whether the two objects are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.hash_value != other.hash_value:
            return False
        
        if self.value != other.value:
            return False
        
        return True
    
    def __repr__(self):
        """Returns the object's representation."""
        return f'{self.__class__.__name__}({self.value!r})'


class GuesserStateNode(RichAttributeErrorBaseType):
    """
    Stores the state of a guesser inside as a node.
    
    Attributes
    ----------
    guesser : ``Guesser``
        The parent guesser instance form what the state inherits from-
    node : ``SubNodeBase``
        Guess node if applicable.
    total_guess_chance : `int`
        The total amount of guess chances.
    """
    __slots__ = ('guesser', 'node', 'total_guess_chance', )
    
    def __new__(cls, guesser):
        """
        Creates a new guess state node instance.
        """
        self = object.__new__(cls)
        self.guesser = guesser
        self.node = None
        self.total_guess_chance = 0
        return self
    
    
    def feed(self, name, value, chance):
        """
        Feeds a result to the guess state node.
        
        Parameters
        ----------
        name : `str`
            The field's name.
        value : `object`
            The field's value.
        chance : `int`
            Matching chance.
        """
        self.total_guess_chance += chance
        
        node = self.node
        if (node is None):
            sub_node_type = self.guesser.sub_node_type
            if (sub_node_type is not None):
                node = sub_node_type(name)
                self.node = node
        
        if (node is not None):
            node.feed(value)
    
    
    def render_into(self, into, indent):
        """
        Renders the node of the guess state if applicable.
        
        Parameters
        ----------
        best_guess_state_node : `None` or ``GuesserStateNode``
            The guesser which scored the highest chance.
        best_chance : `float`
            The scored chance without the applied multiplier.
        """
        node = self.node
        if (node is not None):
            node.render_into(into, indent)


def received_values_most_common_sort_key(item):
    """
    Sort key used when sorting received values by their appearance.
    
    Parameters
    ----------
    items : `tuple` (`object`, `int`)
        Item to return sort key of.
    
    Returns
    -------
    value : `int`
        The value to use as sort key.
    """
    key, value = item
    if key is None:
        value = (1<<63)-1
    
    return value


class ReceivedValueSorter(RichAttributeErrorBaseType):
    """
    Sorter used when sorting received payloads by order.
    
    Attributes
    ----------
    value : `object`
        The stored value.
    """
    __slots__ = ('value',)
    
    def __new__(cls, value):
        """
        Creates a new ``ReceivedValueSorter`` instance with the given `value`.
        
        Parameters
        ----------
        value : `object`
            The value to sort.
        """
        self = object.__new__(cls)
        self.value = value
        return self
    
    def __eq__(self, other):
        """Returns whether the two values are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.value != other.value:
            return False
        
        return True
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_value = self.value
        other_value = other.value
        
        if self_value is None:
            if other_value is None:
                return False
            
            return True
        
        self_value_type = type(self_value)
        other_value_type = type(other_value)
        if self_value_type is other_value_type:
            if self_value > other_value:
                return True
            
            return False
        
        if self_value_type.__name__ > other_value_type.__name__:
            return True
        
        return False


def received_values_order_sort_key(item):
    """
    Sort key used when sorting received values by their order.
    
    Parameters
    ----------
    items : `tuple` (`object`, `int`)
        Item to return sort key of.
    
    Returns
    -------
    value : ``ReceivedValueSorter``
        The value to use as sort key.
    """
    key, value = item
    return ReceivedValueSorter(key)


class GuesserState(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    guessers : `set` of ``GuesserStateNode``
        Then ot yet failed guessers.
    name : `str`
        The node state's name.
    received_count : `int`
        The total amount of received values passed to this node.
    received_values : `None` or `dict` of (`object`, `Any`) items
        The already received values.
    """
    __slots__ = ('guessers', 'name', 'received_count', 'received_values')
    
    def __new__(cls, name):
        """
        Creates a new guess state instance with the given name.
        
        Parameters
        ----------
        name : `str`
            The node state's name.
        """
        self = object.__new__(cls)
        self.name = name
        self.received_values = None
        self.guessers = {GuesserStateNode(guesser) for guesser in GUESSERS}
        self.received_count = 0
        return self
    
    
    def feed(self, value):
        """
        Guesses what type the given value.
        
        Parameters
        ----------
        value : `object`
            The field's value.
        """
        guessers = self.guessers
        if guessers:
            collect_values = False
            guessers_to_remove = None
            
            for guesser_state_node in guessers:
                guesser = guesser_state_node.guesser
                chance = guesser.guesser_function(self.name, value)
                if chance == -1:
                    if (guessers_to_remove is None):
                        guessers_to_remove = []
                    
                    guessers_to_remove.append(guesser_state_node)
                
                else:
                    guesser_state_node.feed(self.name, value, chance)
                    
                    if guesser.collect_values:
                        collect_values = True
            
            if (guessers_to_remove is not None):
                for guesser in guessers_to_remove:
                    guessers.discard(guesser)
        
        else:
            collect_values = True
        
        # count how much times we received this payload.
        
        if collect_values:
            value = freeze(value)
        
            received_values = self.received_values
            if (received_values is None):
                received_values = {}
                self.received_values = received_values
            
            try:
                received_count = received_values[value]
            except KeyError:
                received_count = 1
            else:
                received_count += 1
            
            received_values[value] = received_count
        
        else:
            self.received_values = None
        
        self.received_count += 1
    
    
    def get_most_accurate_guesser(self):
        """
        Tries to get the best fitting guesser node by chance.
        
        Returns
        -------
        best_guess_state_node : `None` or ``GuesserStateNode``
            The guesser which scored the highest chance.
        best_chance : `float`
            The scored chance without the applied multiplier.
        """
        best_chance = -1
        best_guesser = -1
        best_multiplier = 1.0
        
        for guesser_state_node in self.guessers:
            chance = guesser_state_node.total_guess_chance/guesser_state_node.guesser.guess_max_chance
            
            multiplier = 1.0
            parents = guesser_state_node.guesser.parents
            if (parents is not None):
                multiplier += len(parents)*GUESS_CHANCE_MULTIPLIER_BY_PARENT
            
            total_chance = chance*multiplier
            
            if total_chance > best_chance:
                best_chance = total_chance
                best_guesser = guesser_state_node
                best_multiplier = multiplier
        
        return best_guesser, best_chance/best_multiplier
    
    
    def get_most_common_values(self):
        """
        Returns the 5 most common received values.
        
        Returns
        -------
        items : `None` or `list` of `object`
        """
        received_values = self.received_values
        
        if (received_values is None):
            items = None
        else:
            items = sorted(received_values.items(), key=received_values_most_common_sort_key, reverse=True)[:5]
        
        return items
    
    
    def get_all_values(self):
        """
        Returns all the received values sorted by their value.
        
        Returns
        -------
        items : `None` or `list` of `object`
        """
        received_values = self.received_values
        
        if (received_values is None):
            items = None
        else:
            items = sorted(received_values.items(), key=received_values_order_sort_key, reverse=True)[:5]
        
        return items
    
    
    def render_most_common_values_into(self, into, indent):
        """
        Renders the most common values into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        """
        self.render_received_items_into(into, indent, self.get_most_common_values())
    
    
    def render_received_items_into(self, into, indent, items):
        """
        Renders given items into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        items : `tuple` of (`object`, `int`) items
            The items to render.
        """
        if (items is not None):
            received_count = self.received_count
            
            into.append('\n')
            
            for counter in range(indent+1):
                into.append(INDENT)
            
            into.append('values: [\n')
            
            for value, count in items:
                for counter in range(indent+2):
                    into.append(INDENT)
                
                into.append(reprlib.repr(value))
                
                into.append(' (')
                into.append(str(floor(100*count/received_count)))
                into.append('%),\n')
            
            
            for counter in range(indent+1):
                into.append(INDENT)
            
            into.append(']')
    
    
    def render_all_values_into(self, into, indent):
        """
        Renders all the values into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        """
        self.render_received_items_into(into, indent, self.get_all_values())
    
    
    def render_most_commons_into(self, into, indent):
        """
        Renders the most common values of the guesser state into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        """
        best_guesser, best_chance = self.get_most_accurate_guesser()
        self.render_most_commons_into_with_guesser(into, indent, best_guesser)
        
    def render_most_commons_into_with_guesser(self, into, indent, best_guesser):
        """
        Renders the most common values of the guesser state into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        best_guesser : `None` or ``GuesserStateNode``
            The node matching the represented values the most.
        """
        if (best_guesser is None):
            self.render_most_common_values_into(into, indent)
        else:
            guesser = best_guesser.guesser
            if guesser.render_all_values:
                self.render_all_values_into(into, indent)
            elif guesser.collect_values:
                self.render_most_common_values_into(into, indent)
    
    
    def render_into(self, into, indent, inline):
        """
        Renders the guesser state into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts to.
        indent : `int`
            The indention level of the field.
        inline : `bool`
            Whether the rendering should be started inline. This might be used by nested renderers.
        """
        best_guesser, best_chance = self.get_most_accurate_guesser()
        
        if not inline:
            for counter in range(indent):
                into.append(INDENT)
            
            into.append(self.name)
            into.append(': ')
        
        if best_guesser is None:
            into.append(UNKNOWN_FIELD_TYPE_NAME)
        else:
            into.append(best_guesser.guesser.name)
            into.append(' (')
            percentage = floor(100*best_chance/self.received_count)
            into.append(str(percentage))
            into.append('%)')
        
        if not inline:
            self.render_most_commons_into_with_guesser(into, indent, best_guesser)
            
        best_guesser.render_into(into, indent)


GUESSERS_BY_EVENT = {}

def guess_event_payload_structure(event_name, payload):
    """
    Guesses the event payload's structure.
    
    Parameters
    ----------
    event_name : `str`
        The respective event's name.
    payload : `object`
        The received payload.
    """
    try:
        guesser = GUESSERS_BY_EVENT[event_name]
    except KeyError:
        guesser = GuesserState(event_name)
        GUESSERS_BY_EVENT[event_name] = guesser
    
    guesser.feed(payload)


def render_payload_states():
    """
    Renders the already collected payloads.
    
    Returns
    -------
    structure : `str`
        The rendered structure.
    """
    into = []
    
    for guesser in GUESSERS_BY_EVENT.values():
        guesser.render_into(into, 0, False)
    
    into.append('\n')
    return ''.join(into)


def test():
    TEXT_PAYLOAD_EVENT_NAME = 'EMBEDDED_ACTIVITY_UPDATE'
    
    TEST_PAYLOADS = [
        {'users': [], 'guild_id': '817005167500984320', 'embedded_activity': {'application_id': '814288819477020702'}, 'channel_id': '881247624009756713'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Poker', 'secrets': {'join': '154ce3b8915f70fe1afbf903bffa224e073b62f70be3a9dbe714eced'}, 'name': 'Poker Night', 'details': None, 'created_at': None, 'assets': {'small_text': 'Poker Night', 'large_text': 'Poker Night', 'large_image': '839608726894018561'}, 'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281', '197918569894379520'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Poker', 'secrets': {'join': '154ce3b8915f70fe1afbf903bffa224e073b62f70be3a9dbe714eced'}, 'name': 'Poker Night', 'details': None, 'created_at': None, 'assets': {'small_text': 'Poker Night', 'large_text': 'Poker Night', 'large_image': '839608726894018561'}, 'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281', '197918569894379520'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Poker', 'secrets': {'join': '154ce3b8915f70fe1afbf903bffa224e073b62f70be3a9dbe714eced'}, 'name': 'Poker Night', 'details': None, 'created_at': None, 'assets': {'small_text': 'Playing Poker', 'large_text': 'Playing Poker', 'large_image': '839608726894018561'}, 'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Poker', 'secrets': {'join': '154ce3b8915f70fe1afbf903bffa224e073b62f70be3a9dbe714eced'}, 'name': 'Poker Night', 'details': None, 'created_at': None, 'assets': {'small_text': 'Playing Poker', 'large_text': 'Playing Poker', 'large_image': '839608726894018561'}, 'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': None, 'timestamps': None, 'state': None, 'secrets': None, 'name': 'Poker Night', 'details': None, 'created_at': None, 'assets': None, 'application_id': '755827207812677713'}, 'channel_id': '388267637236563971'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640368980971}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': 'Playing game', 'created_at': None, 'assets': {'small_text': 'Chess', 'large_text': 'Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640368980971}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': 'Playing game', 'created_at': None, 'assets': {'small_text': 'Chess', 'large_text': 'Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640365324274}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': 'Playing game', 'created_at': None, 'assets': {'small_text': 'Chess', 'large_text': 'Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640365308863}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': 'Playing Game', 'created_at': None, 'assets': {'small_text': 'Chess', 'large_text': 'Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640368864117}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': None, 'created_at': None, 'assets': {'small_text': 'Playing Chess', 'large_text': 'Playing Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '773336526917861400'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': {'start': 1640368864117}, 'state': 'Playing Chess', 'secrets': {'join': 'ca61affe377ddb3aaf8123eb5a31217dd5a0327dd69d22a04265fd70'}, 'name': 'Chess In The Park', 'details': None, 'created_at': None, 'assets': {'small_text': 'Playing Chess', 'large_text': 'Playing Chess', 'large_image': '853007059326992414'}, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': None, 'timestamps': None, 'state': None, 'secrets': None, 'name': 'Chess In The Park', 'details': None, 'created_at': None, 'assets': None, 'application_id': '832012774040141894'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Betrayal.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io', 'large_image': '783066688958103632'}, 'application_id': '773336526917861400'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Betrayal.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io', 'large_image': '783066688958103632'}, 'application_id': '773336526917861400'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Betrayal.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io', 'large_image': '783066688958103632'}, 'application_id': '773336526917861400'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': None, 'timestamps': None, 'state': None, 'secrets': None, 'name': 'Betrayal.io', 'details': None, 'created_at': None, 'assets': None, 'application_id': '773336526917861400'}, 'channel_id': '388267637236563971'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Creating Party', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Creating Party', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['197918569894379520', '184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:ILSEYK'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Relaxing', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': None, 'timestamps': None, 'state': None, 'secrets': None, 'name': 'Fishington.io', 'details': None, 'created_at': None, 'assets': None, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Playing Fishing', 'secrets': {'join': 'server:TPGZMU'}, 'name': 'Fishington.io', 'details': 'In-Game', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': 0, 'timestamps': None, 'state': 'Creating Party', 'secrets': None, 'name': 'Fishington.io', 'details': 'In Menu', 'created_at': None, 'assets': {'small_text': 'Betrayal.io', 'large_text': 'Betrayal.io'}, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': ['184734189386465281'], 'guild_id': '388267636661682178', 'embedded_activity': {'type': None, 'timestamps': None, 'state': None, 'secrets': None, 'name': 'Fishington.io', 'details': None, 'created_at': None, 'assets': None, 'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
        {'users': [], 'guild_id': '388267636661682178', 'embedded_activity': {'application_id': '814288819477020702'}, 'channel_id': '388267637236563971'},
    ]

    for payload in TEST_PAYLOADS:
        guess_event_payload_structure(TEXT_PAYLOAD_EVENT_NAME, payload)
    
    print(render_payload_states())

if __name__ == '__main__':
    test()
