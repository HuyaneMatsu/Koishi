__all__ = ()

from datetime import timezone as TimeZone

from sqlalchemy import (
    BIGINT as Int64, Column, DateTime, Integer as Int32, LargeBinary as Binary, SmallInteger as Int16
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE


QUEST_TEMPLATE_ID_TO_ITEM_ID = {
    1 : (1, 1),
    2 : (2, 1),
    3 : (3, 2),
    4 : (4, 2),
    5 : (4, 2),
    6 : (5, 2),
    7 : (7, 2),
    8 : (8, 2),
    9 : (9, 2),
    10 : (10, 2),
    11 : (5, 1),
    12 : (6, 1),
    13 : (18, 1),
    14 : (18, 1),
    15 : (22, 2),
    16 : (21, 2),
    17 : (21, 2),
    18 : (17, 1),
    19 : (22, 2),
    20 : (28, 1),
    21 : (28, 1),
    22 : (27, 1),
    23 : (9, 2),
    24 : (31, 1),
    25 : (21, 1),
    26 : (1, 2),
}


def _get_combined_model():
    """
    Gets a combined model with the new and the old quest fields.
    
    Returns
    -------
    linked_quest_model_combined : ``DeclarativeMeta``
    """
    class linked_quest_model_combined(declarative_base()):
        __tablename__      = 'LINKED_QUESTS'
        # Staying
        id                 = Column(Int64, primary_key = True)
        batch_id           = Column(Int64, default = 0, nullable = False)
        guild_id           = Column(Int64, default = 0, nullable = False)
        template_id        = Column(Int64, default = 0, nullable = False)
        user_id            = Column(Int64, default = 0, nullable = False)
        completion_state   = Column(Int16, default = 1, nullable = False)
        completion_count   = Column(Int32, default = 0, nullable = False)
        
        # Old
        taken_at           = Column(DateTime, nullable = False)
        expires_at         = Column(DateTime, nullable = False)
        
        amount_required    = Column(Int64, default = 0, nullable = False)
        amount_submitted   = Column(Int64, default = 0, nullable = False)
        
        reward_balance     = Column(Int64, default = 0, nullable = False)
        reward_credibility = Column(Int64, default = 0, nullable = False)
        
        # New
        requirements       = Column(Binary(), default = None, nullable = True)
        rewards            = Column(Binary(), default = None, nullable = True)
    
    
    return linked_quest_model_combined


def execute_migration():
    """
    Executes the migration.
    """
    linked_quest_model_combined = _get_combined_model()
    
    with DB_ENGINE.connect() as connector:
        
        # ---- Query quests. ----
        
        response = connector.execute(
            select(
                [
                    linked_quest_model_combined.id,
                    linked_quest_model_combined.template_id,
                    linked_quest_model_combined.taken_at,
                    linked_quest_model_combined.expires_at,
                    linked_quest_model_combined.amount_required,
                    linked_quest_model_combined.amount_submitted,
                    linked_quest_model_combined.reward_balance,
                    linked_quest_model_combined.reward_credibility,
                ],
            ),
        )
        entries = response.fetchall()
        
        # ---- Insert quests. ----
        
        for (
            entry_id,
            template_id,
            taken_at,
            expires_at,
            amount_required,
            amount_submitted,
            reward_balance,
            reward_credibility,
        ) in entries:
            item_id, amount_type = QUEST_TEMPLATE_ID_TO_ITEM_ID.get(template_id, (1, 1))
            
            requirements = b''.join([
                # Duration
                (5).to_bytes(1, 'little'),
                int((expires_at - taken_at).total_seconds()).to_bytes(8, 'little'),
                # Expiration
                (4).to_bytes(1, 'little'),
                int(expires_at.replace(tzinfo = TimeZone.utc).timestamp()).to_bytes(8, 'little'),
                # Item exact
                (1).to_bytes(1, 'little'),
                item_id.to_bytes(4, 'little'),
                amount_type.to_bytes(1, 'little'),
                amount_required.to_bytes(8, 'little'),
                amount_submitted.to_bytes(8, 'little'),
            ])
            
            rewards = b''.join([
                # Balance
                (1).to_bytes(1, 'little'),
                reward_balance.to_bytes(8, 'little'),
                # Credibility
                (2).to_bytes(1, 'little'),
                reward_credibility.to_bytes(8, 'little'),
            ])
            
            connector.execute(
                linked_quest_model_combined.__table__.update().values(
                    requirements = requirements,
                    rewards = rewards,
                ).where(
                    linked_quest_model_combined.id == entry_id,
                )
            )
