__all__ = ()

from hata.main import register

from .relationships_rework_2026_01_29 import execute_migration as execute_migration_relationships_rework_2026_01_29
from .quest_reword_2026_03_10 import execute_migration as execute_migration_quest_reword_2026_03_10
from .notification_rework_2026_05_02 import execute_migration as execute_migration_notification_rework_2026_05_02


MIGRATIONS = (
    ('relationships_rework_2026_01_29', execute_migration_relationships_rework_2026_01_29),
    ('quest_reword_2026_03_10', execute_migration_quest_reword_2026_03_10),
    ('notification_rework_2026_05_02', execute_migration_notification_rework_2026_05_02),
)


@register
def migrate(
    migration_name : str,
):
    """
    Executes a database migration.
    
    Adding the new fields before and removing the old fields after is on you.
    """
    for iterated_migration_name, executor in MIGRATIONS:
        if iterated_migration_name == migration_name:
            break
    else:
        return ''.join([
            f'Migration {migration_name!s} does not exist. The available migrations are the following:',
            *(f'\n- {item[0]!s}' for item in MIGRATIONS)
        ])
    
    executor()
    return 'Database migration executed.'
