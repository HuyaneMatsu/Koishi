__all__ = ('QuestBatch', 'quest_batch_create')

from scarletio import RichAttributeErrorBaseType


class QuestBatch(RichAttributeErrorBaseType):
    """
    Represents a batch of quests.
    
    Attributes
    ----------
    id : `int`
        The identifier of the match. Used for deduplication.
    
    quests : ``tuple<Quest>``
        The quests of the batch.
    """
    __slots__ = ('id', 'quests')
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # quests
        repr_parts.append(', quests = ')
        repr_parts.append(repr(self.quests))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def quest_batch_create(batch_id, quests):
    """
    Creates a new quest batch.
    
    Parameters
    ----------
    batch_id : `int`
        The identifier of the batch. Used for deduplication.
    
    quests : ``tuple<Quest>``
        The quests of the batch.
    
    Returns
    -------
    quest_batch : ``QuestBatch``
    """
    quest_batch = object.__new__(QuestBatch)
    quest_batch.id = batch_id
    quest_batch.quests = quests
    return quest_batch
