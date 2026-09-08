__all__ = ()

from ...bot_utils.models import DB_ENGINE, linked_quest_model


def execute_migration():
    """
    Executes the migration.
    """
    with DB_ENGINE.connect() as connector:
        connector.execute(
            linked_quest_model.__table__.update().values(
                created_at = linked_quest_model.created_at / 1_000_000_000
            ).where(
                linked_quest_model.created_at > 1888888888888
            )
        )
