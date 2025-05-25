import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_question_stat_upgrade_purchase_self
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    yield (
        2,
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = 'stats.upgrade.confirm.self.2',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = 'stats.upgrade.cancel.self.2',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_stat_upgrade_purchase_self(stat_index):
    """
    tests whether ``build_component_question_stat_upgrade_purchase_self`` works as intended.
    
    Parameters
    ----------
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_stat_upgrade_purchase_self(stat_index)
    vampytest.assert_instance(output, Component)
    return output
