__all__ = ()

from struct import Struct

from sqlalchemy.sql import select

from ...bot_utils.models import (
    DB_ENGINE, RELATIONSHIP_REQUEST_TABLE, RELATIONSHIP_TABLE, USER_BALANCE_TABLE, relationship_model,
    relationship_request_model, user_balance_model
)


ALLOCATION_STRUCT = Struct(b'<HQQ')
ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST = 3


def execute_migration():
    """
    Executes the migration.
    """
    with DB_ENGINE.connect() as connector:
        # ---- Update the requests. ----
    
        # I could not figure out how to do the shifting, so I load everything instead.
        response = connector.execute(
            select(
                [
                    relationship_request_model.id,
                    relationship_request_model.relationship_type,
                ]
            )
        )
        entries = response.fetchall()
        
        for entry_id, relationship_type in entries:
            connector.execute(
                RELATIONSHIP_REQUEST_TABLE.update().values(
                    relationship_type = 1 << relationship_type,
                ).where(
                    relationship_request_model.id == entry_id,
                )
            )
        
        # ---- Update the relationships. ----
        
        response = connector.execute(
            select(
                [
                    relationship_model.id,
                    relationship_model.relationship_type,
                ]
            )
        )
        entries = response.fetchall()
        
        for entry_id, relationship_type in entries:
            connector.execute(
                RELATIONSHIP_TABLE.update().values(
                    relationship_type = 1 << relationship_type,
                ).where(
                    relationship_model.id == entry_id,
                )
            )
        
        # ---- Update the user balance. ----
        
        response = connector.execute(
            select(
                [
                    relationship_request_model.id,
                    relationship_request_model.source_user_id,
                    relationship_request_model.investment,
                ]
            )
        )
        entries = response.fetchall()
        
        for entry_id, source_user_id, investment in entries:
            response = connector.execute(
                select(
                    [
                        user_balance_model.id,
                        user_balance_model.balance,
                        user_balance_model.allocations,
                    ]
                ).where(
                    user_balance_model.user_id == source_user_id
                )
            )
            
            user_balance_entry_id, balance, allocations = response.fetchone()
            allocation = ALLOCATION_STRUCT.pack(ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, entry_id, investment)
            
            connector.execute(
                USER_BALANCE_TABLE.update().values(
                    balance = balance + investment,
                    allocations = (allocation if allocations is None else allocations + allocation),
                ).where(
                    user_balance_model.id == user_balance_entry_id,
                )
            )
