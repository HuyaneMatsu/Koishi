__all__ = ()

from hata import Emoji
from hata.ext.slash import Button, Option, Row, Select

import config

from ...bot_utils.constants import (
    ROLE__SUPPORT__BOT_ACCESS__ALICE, ROLE__SUPPORT__BOT_ACCESS__FLANDRE, ROLE__SUPPORT__BOT_ACCESS__KOISHI,
    ROLE__SUPPORT__BOT_ACCESS__ORIN, ROLE__SUPPORT__BOT_ACCESS__TOY_KOISHI, ROLE__SUPPORT__BOT_ACCESS__YOSHIKA
)


CLAIM_ROLE_VERIFIED_EMOJI = Emoji.precreate(931503291957919744)
CUSTOM_ID_CLAIM_ROLE_VERIFIED = 'rules.claim_role.verified'

CLAIM_ROLE_ANNOUNCEMENTS_EMOJI = Emoji.precreate(1175518140390707332)
CUSTOM_ID_CLAIM_ROLE_ANNOUNCEMENTS = 'rules.claim_role.announcements'

CLAIM_ROLE_POLLS_EMOJI = Emoji.precreate(1087715009045479465)
CUSTOM_ID_CLAIM_ROLE_POLLS = 'rules.claim_role.polls'

CUSTOM_ID_CLAIM_ROLE_BOT_ACCESS = 'rules.bot_select'


RULES_COMPONENTS = [
    Row(
        Button(
            'Accept rules (I wont fry fumos)',
            CLAIM_ROLE_VERIFIED_EMOJI,
            custom_id = CUSTOM_ID_CLAIM_ROLE_VERIFIED,
        ),
        Button(
            'Claim announcements role',
            CLAIM_ROLE_ANNOUNCEMENTS_EMOJI,
            custom_id = CUSTOM_ID_CLAIM_ROLE_ANNOUNCEMENTS,
        ),
        Button(
            'Claim polls role',
            CLAIM_ROLE_POLLS_EMOJI,
            custom_id = CUSTOM_ID_CLAIM_ROLE_POLLS,
        ),
    ),
    Row(
        Select(
            [
                Option(
                    str(config.ALICE_ID),
                    'Alice',
                ),
                Option(
                    str(config.FLANDRE_ID),
                    'Flandre',
                ),
                Option(
                    str(config.KOISHI_ID),
                    'Koishi',
                ),
                Option(
                    str(config.ORIN_ID),
                    'Orin',
                ),
                Option(
                    str(config.TOY_KOISHI_ID),
                    'Toy Koishi',
                ),
                Option(
                    str(config.YOSHIKA_ID),
                    'Yoshika',
                ),
            ],
            CUSTOM_ID_CLAIM_ROLE_BOT_ACCESS,
            placeholder = 'Select a bot of your preference'
        ),
    ),
]


BOT_ACCESS_ROLES = {
    config.ALICE_ID : ROLE__SUPPORT__BOT_ACCESS__ALICE,
    config.FLANDRE_ID : ROLE__SUPPORT__BOT_ACCESS__FLANDRE,
    config.KOISHI_ID : ROLE__SUPPORT__BOT_ACCESS__KOISHI,
    config.ORIN_ID : ROLE__SUPPORT__BOT_ACCESS__ORIN,
    config.TOY_KOISHI_ID : ROLE__SUPPORT__BOT_ACCESS__TOY_KOISHI,
    config.YOSHIKA_ID : ROLE__SUPPORT__BOT_ACCESS__YOSHIKA,
}
