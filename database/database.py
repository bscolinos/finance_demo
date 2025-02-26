# database/database.py
import singlestoredb as s2
from tradeSimulator.config import Config
from database.models import CREATE_LIVE_TRADES_TABLE

def init_db():
    # Replace protocol if needed
    db_url = Config.get_singlestore_db_url()
    conn = s2.connect(db_url)
    cur = conn.cursor()
    try:
        cur.execute(CREATE_LIVE_TRADES_TABLE)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cur.close()
        conn.close()
