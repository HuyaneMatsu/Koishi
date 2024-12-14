__all__ = ('propose',)

from math import floor

from hata import Client, Embed
from hata.ext.slash import InteractionResponse
from sqlalchemy import or_
from sqlalchemy.sql import select

from ....bot_utils.models import DB_ENGINE, waifu_list_model
from ....bot_utils.constants import EMOJI__HEART_CURRENCY, WAIFU_COST_DEFAULT
from ....bot_utils.user_getter import get_user

from ..constants.waifu_type import get_relation_name
from ..helpers import get_multiplier


def propose(
    client,
    event,
    user: ('user', 'The user to propose to.'),
    amount: ('int', 'The amount of love to propose with.'),
):
    """Propose marriage to a user."""
    
