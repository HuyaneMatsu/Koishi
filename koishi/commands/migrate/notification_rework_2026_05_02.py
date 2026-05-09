__all__ = ()


from sqlalchemy import BIGINT as Int64, Boolean, Column, SmallInteger as Int16
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE


USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU = 1
USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER = 2
USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT = 3
USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL = 5
USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE = 6

USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX = 1


def _get_combined_model():
    """
    Gets a combined model with the new and the old quest fields.
    
    Returns
    -------
    user_settings_model_combined : ``DeclarativeMeta``
    """
    class user_settings_model_combined(declarative_base()):
        __tablename__ = 'USER_SETTINGS'
        
        # Staying
        id = Column(Int64, nullable = False, primary_key = True)
        user_id = Column(Int64, nullable = False)
        preferred_client_id = Column(Int64, default = 0, nullable = False)
        preferred_image_source = Column(Int16, default = 0, nullable = False)
        
        # Old
        
        notification_daily_by_waifu = Column(Boolean, default = True, nullable = False)
        notification_daily_reminder = Column(Boolean, default = False, nullable = False)
        notification_gift = Column(Boolean, default = True, nullable = False)
        notification_proposal = Column(Boolean, default = True, nullable = False)
        notification_vote = Column(Boolean, default = True, nullable = False)
        
        # New
        notification_flags = Column(Int64, default = 0, nullable = False)
        feature_flags = Column(Int64, default = 0, nullable = False)
    
    return user_settings_model_combined


def execute_migration():
    """
    Executes the migration.
    """
    user_settings_model_combined = _get_combined_model()
    
    with DB_ENGINE.connect() as connector:
        
        # ---- Query user settings. ----
        
        response = connector.execute(
            select(
                [
                    user_settings_model_combined.id,
                    user_settings_model_combined.notification_daily_by_waifu,
                    user_settings_model_combined.notification_daily_reminder,
                    user_settings_model_combined.notification_gift,
                    user_settings_model_combined.notification_proposal,
                    user_settings_model_combined.notification_vote,
                ],
            ),
        )
        entries = response.fetchall()
        
        # ---- Insert user settings. ----
        
        for (
            entry_id,
            notification_daily_by_waifu,
            notification_daily_reminder,
            notification_gift,
            notification_proposal,
            notification_vote,
        ) in entries:
            notification_flags = (
                (notification_daily_by_waifu << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU) |
                (notification_daily_reminder << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER) |
                (notification_gift << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT) |
                (notification_proposal << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL) |
                (notification_vote << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE)
            )

            connector.execute(
                user_settings_model_combined.__table__.update().values(
                    notification_flags = notification_flags,
                ).where(
                    user_settings_model_combined.id == entry_id,
                )
            )
        
        # ---- Update user settings with feature flags. -----
        
        feature_flags = 1 << USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX
        
        connector.execute(
            user_settings_model_combined.__table__.update().values(
                feature_flags = feature_flags,
            ),
        )
