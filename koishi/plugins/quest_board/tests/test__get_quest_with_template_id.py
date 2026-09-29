import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    Quest, get_quest_template_nullable, quest_batch_create, quest_create
)

from ..helpers import get_quest_with_template_id


def _iter_options():
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template_nullable(quest_template_id_0)
    assert quest_template_0 is not None
    
    quest_0 = quest_create(
        quest_template_id_0,
        None,
        None,
    )
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template_nullable(quest_template_id_1)
    assert quest_template_1 is not None
    
    quest_1 = quest_create(
        quest_template_id_1,
        None,
        None,
    )
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template_nullable(quest_template_id_2)
    assert quest_template_2 is not None
    
    quest_2 = quest_create(
        quest_template_id_2,
        None,
        None,
    )
    
    yield (
        quest_batch_create(
            123,
            (
                quest_0,
                quest_1,
                quest_2,
            ),
        ),
        quest_template_id_1,
        quest_1,
    )
    
    yield (
        quest_batch_create(
            124,
            (
                quest_0,
                quest_1,
            ),
        ),
        quest_template_id_2,
        None,
    )
    
    yield (
        quest_batch_create(
            125,
            (),
        ),
        quest_template_id_0,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_with_template_id(quest_batch, quest_template_id):
    """
    Tests whether ``get_quest_with_template_id`` works as intended.
    
    Parameters
    ----------
    quest_batch : ``QuestBatch``
        Quest batch to get the quest from.
    
    quest_template_id : `int`
        The quest template's identifier.
    
    Returns
    -------
    output : ``None | Quest``
    """
    output = get_quest_with_template_id(quest_batch, quest_template_id)
    vampytest.assert_instance(output, Quest, nullable = True)
    return output
