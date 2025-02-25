__all__ = ('CooldownHandler',)

from hata import KOKORO, Message
from scarletio import LOOP_TIME


class CooldownUnit:
    """
    A cooldown unit stored by a ``CommandCooldownWrapper``-s.
    
    Attributes
    ----------
    expires_at : `float`
        When the cooldown unit will expire in LOOP_TIME time.
    uses_left : `int`
        How much uses are left till the respective entity will be locked by cooldown.
    """
    __slots__ = ('expires_at', 'uses_left',)
    
    def __init__(self, expires_at, uses_left):
        """
        Creates a new ``CooldownUnit`` with the given parameters.
        
        Parameters
        ----------
        expires_at : `float`
            When the cooldown unit will expire in LOOP_TIME time.
        uses_left : `int`
            How much uses are left till the respective entity will be locked by cooldown.
        """
        self.expires_at = expires_at
        self.uses_left = uses_left
    
    def __repr__(self):
        """Returns the object's representation."""
        return f'{type(self).__name__!s}(expires_at = {self.expires_at!r}, uses_left = {self.uses_left!r})'


def _check_user(cooldown_handler, event_or_message, weight):
    """
    Executes user cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    event_or_message : ``InteractionEvent``, ``Message``
        The event or message to get the cooldown for.
    weight : `int`
        The weight to use.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
    """
    if isinstance(event_or_message, Message):
        user_id = event_or_message.author.id
    else:
        user_id = event_or_message.user.id
    
    cache = cooldown_handler.cache
    try:
        unit = cache[user_id]
    except KeyError:
        at_ = LOOP_TIME() + cooldown_handler.reset
        cache[user_id] = CooldownUnit(at_, cooldown_handler.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, user_id)
        return 0.0
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left - weight
        return 0.0
    
    return unit.expires_at


def _check_channel(cooldown_handler, event_or_message, weight):
    """
    Executes channel cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    event_or_message : ``InteractionEvent``, ``Message``
        The event or message to get the cooldown for.
    weight : `int`
        The weight to use.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
    """
    channel_id = event_or_message.channel_id
    
    cache = cooldown_handler.cache
    try:
        unit = cache[channel_id]
    except KeyError:
        at_ = LOOP_TIME() + cooldown_handler.reset
        cache[channel_id] = CooldownUnit(at_, cooldown_handler.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, channel_id)
        return 0.
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left - weight
        return 0.0
    
    return unit.expires_at


def _check_guild(cooldown_handler, event_or_message, weight):
    """
    Executes guild based cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    event_or_message : ``InteractionEvent``, ``Message``
        The event or message to get the cooldown for.
    weight : `int`
        The weight to use.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
        
        If the cooldown limitation is not applicable for the given entity, returns `-1.0`.
    """
    guild_id = event_or_message.guild_id
    if not guild_id:
        return -1.0
    
    cache = cooldown_handler.cache
    try:
        unit = cache[guild_id]
    except KeyError:
        at_ = LOOP_TIME() + cooldown_handler.reset
        cache[guild_id] = CooldownUnit(at_, cooldown_handler.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, guild_id)
        return 0.0
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left - weight
        return 0.0
    
    return unit.expires_at


class CooldownHandler:
    """
    Cooldown for commands.
    
    Attributes
    ----------
    cache : `dict` of (``DiscordEntity``, ``CooldownUnit``) items
        Cache to remember how much use of the given entity are exhausted already.
    checker : `function`
        Checks after how much time the given entity can use again the respective command.
    limit : `int`
        The amount of how much times the command can be called within a set duration before going on cooldown.
    reset : `float`
        The time after the cooldown resets.
    weight : `int`
        The weight of the command.
    """
    __slots__ = ('cache', 'checker', 'limit', 'reset', 'weight',)
    
    def __new__(cls, for_, reset, limit = 1, weight = 1):
        """
        Creates a new ``CooldownHandler`` from the given parameters.
        
        Parameters
        ----------
        for_ : `str`
            By what type of entity the cooldown should limit the command.
            
            Possible values:
             - `'user'`
             - `'channel'`
             - `'guild'`
         
        reset : `float`
            The reset time of the cooldown.
        
        limit : `int` = `1`, Optional
            The amount of calls after the respective command goes on cooldown.
        
        weight : `int` = `1`, Optional
            The weight of one call. Defaults to `1`.
        
        Raises
        ------
        TypeError
            - If `str` is not given as `str`.
            - If `weight` is not numeric convertible to `int`.
            - If `reset` is not numeric convertible to `float`.
            - If `limit` is not numeric convertible to `int`.
        ValueError
            - If `for_` is not given as any of the expected value.
        """
        for_type = type(for_)
        if for_type is str:
            pass
        elif issubclass(for_, str):
            for_ = str(for_)
        else:
            raise TypeError(
                f'`for_` can be `str`, got {for_type.__name__}; {for_!r}.'
            )
        
        if 'user'.startswith(for_):
            checker = _check_user
        elif 'channel'.startswith(for_):
            checker = _check_channel
        elif 'guild'.startswith(for_):
            checker = _check_guild
        else:
            raise ValueError(
                f'\'for_\' can be \'user\', \'channel\' or \'guild\', got {for_!r}'
            )
        
        reset_type = reset.__class__
        if (reset_type is not float):
            try:
                __float__ = getattr(reset_type, '__float__')
            except AttributeError:
                raise TypeError(
                    f'The given reset is not `float`, neither other numeric convertible to it, got '
                    f'{reset_type.__name__}; {reset!r}.'
                ) from None
            
            reset = __float__(reset)
            
        limit_type = limit.__class__
        if limit_type is int:
            pass
        elif issubclass(limit_type, int):
            limit = int(limit)
        else:
            raise TypeError(
                f'`limit` can be `int`, got {limit_type.__name__}; {limit!r}.'
            ) from None
        
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(
                f'`weight` can be `int`, got {weight_type.__name__}; {weight!r}.'
            ) from None
        
        self = object.__new__(cls)
        self.checker = checker
        self.reset = reset
        self.weight = weight
        self.limit = limit - weight
        self.cache = {}
        
        return self
    
    
    def get_cooldown(self, event_or_message, weight = -1):
        """
        Returns for how long the cooldown is triggered.
        
        Parameters
        ----------
        event_or_message : ``InteractionEvent``, ``Message``
            The event or message to get the cooldown for.
        
        Returns
        -------
        expires_after : `float`
            After how much time in seconds the cooldown is reset
        """
        if weight < 0:
            weight = self.weight
        
        expires_at = self.checker(self, event_or_message, weight)
        if not expires_at:
            return 0.0
            
        if expires_at == -1.0:
            return - 1.0
        
        return expires_at - LOOP_TIME()

