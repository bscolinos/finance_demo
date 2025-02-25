
import os
import singlestoredb as s2
from datetime import datetime

class TrackingService:
    @staticmethod
    def log_activity(activity_type: str, details: dict = None):
        """Log user activity to database"""
        config = {
            "host": os.getenv('host'),
            "port": os.getenv('port'),
            "user": os.getenv('user'),
            "password": os.getenv('password'),
            "database": os.getenv('database')
        }
        
        connection = s2.connect(**config)
        cursor = connection.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(100),
                activity_type VARCHAR(50),
                details JSON,
                timestamp DATETIME
            )
        """)
        
        # Get user_id from session state
        user_id = st.session_state.get('user_id', 'anonymous')
        
        # Insert activity
        cursor.execute(
            "INSERT INTO user_activities (user_id, activity_type, details, timestamp) VALUES (%s, %s, %s, %s)",
            (user_id, activity_type, str(details), datetime.now())
        )
        
        connection.commit()
        cursor.close()
        connection.close()
