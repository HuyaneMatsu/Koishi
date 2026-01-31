__all__ = ()

from hata.main import register

from .relationships_rework_2026_01_29 import execute_migration as execute_migration_relationships_rework_2026_01_29


MIGRATIONS = (
    ('relationships_rework_2026_01_29', execute_migration_relationships_rework_2026_01_29),
)


@register
def migrate(
    migration_name : str,
):
    """
    Executes a database migration.
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
