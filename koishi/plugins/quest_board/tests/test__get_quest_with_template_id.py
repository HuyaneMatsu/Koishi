import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, Quest,
    QuestBatch, get_quest_template
)

from ..helpers import get_quest_with_template_id


def _iter_options():
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    
    quest_0 = Quest(
        quest_template_id_0,
        quest_amount_0,
        3600,
        2,
        1000,
    )
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    
    quest_1 = Quest(
        quest_template_id_1,
        quest_amount_1,
        3600,
        2,
        1000,
    )
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template(quest_template_id_2)
    assert quest_template_2 is not None
    quest_amount_2 = 174000
    
    quest_2 = Quest(
        quest_template_id_2,
        quest_amount_2,
        3600,
        2,
        1000,
    )
    
    yield (
        QuestBatch(
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
        QuestBatch(
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
        QuestBatch(
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
