__all__ = ()

from scarletio import RichAttributeErrorBaseType


class QuestSubTypeBase(RichAttributeErrorBaseType):
    """
    Base type for quest sub-types.
    """
    __slots__ = ()
    
    TYPE = 0
    
    def __repr__(self):
        """Returns repr(self)."""
        return ''.join(['<', type(self).__name__, *self._produce_representation_middle(), '>'])
    
    
    def _produce_representation_middle(self):
        """
        Helper to produce the middle of the instance's representation.
        
        This function is an iterable generator.
        
        Yields
        ------
        part : `str`
        """
        return
        yield
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Helper method to return whether the two instances are same.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True


class QuestSubTypeGenerator(QuestSubTypeBase):
    """
    Base type for quest sub-types which can generate.
    """
    __slots__ = ()
    
    def generate(self, random_number_generator):
        """
        Generates a new value defined by self.
        
        Parameters
        ----------
        random_number_generator : `random.Random`
            Random number generator to use.
        
        Returns
        -------
        generated_and_diversion : ``(QuestSubTypeInstantiable, float)``
        """
        return (
            QuestSubTypeInstantiable(),
            1.0,
        )
    
    
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        """
        Generates a new value defined by self.
        
        Parameters
        ----------
        random_number_generator : `random.Random`
            Random number generator to use.
        
        accumulated_diversion : `float`
            Already accumulated diversion.
        
        Returns
        -------
        generated_and_diversion : ``(QuestSubTypeInstantiable, float)``
        """
        return self.generate(random_number_generator)


class QuestSubTypeInstantiable(QuestSubTypeBase):
    """
    Base type for quest sub-types which can be instantiated.
    """
    __slots__ = ()
    
    def instantiate(self):
        """
        Instantiates the quest requirement.
        
        Returns
        -------
        instance : ``QuestSubTypeSerialisable``
        """
        return QuestSubTypeSerialisable()


class QuestSubTypeSerialisable(QuestSubTypeBase):
    """
    Base type for quest sub-types which can be serialised.
    """
    __slots__ = ()
    
    @classmethod
    def deserialise(cls, data, start_index):
        """
        Creates a new quest requirement completion state from the given raw data.
        
        Parameters
        ----------
        data : `memoryview`
            Data to parse from.
        
        start_index : `int`
            Index to start parsing at.
        
        Returns
        -------
        self_and_end_index : `None | (instance<cls>, int>)`
        """
        return object.__new__(cls), start_index
    
    
    def serialise(self):
        """
        Serialises self.
        
        This method is an iterable generator.
        
        Yields
        ------
        part : `bytes`
        """
        return
        yield
