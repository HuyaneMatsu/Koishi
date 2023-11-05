__all__ = ('ChatInteraction',)

from scarletio import RichAttributeErrorBaseType


class ChatInteraction(RichAttributeErrorBaseType):
    """
    Represents a chat interaction.
    
    Attributes
    ----------
    check_can_trigger : `FunctionType`
        A check returning whether the interaction can be triggered.
        Should return non-null value when can be triggered.
    
    name : `str`
        The name of the chat interaction.
    
    trigger : `CoroutineFuntionType`
        Function used for triggering.
    """
    __slots__ = ('check_can_trigger', 'name', 'trigger')
    
    def __new__(cls, name, check_can_trigger, trigger):
        """
        Creates a new chat interaction with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the chat interaction.
        check_can_trigger : `FunctionType`
            A check returning whether the interaction can be triggered.
        trigger : `CoroutineFuntionType`
            Function used for triggering.
        """
        self = object.__new__(cls)
        self.name = name
        self.check_can_trigger = check_can_trigger
        self.trigger = trigger
        return self
    
    
    def __repr__(self):
        """Returns the chat interaction's representation."""
        return ''.join(['<', self.__class__.__name__, ' name = ', repr(self.name), '>'])
