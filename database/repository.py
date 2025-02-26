# database/repository.py
import singlestoredb as s2
import pandas as pd
from tradeSimulator.config import Config

class TradeRepository:
    def __init__(self):
        db_url = Config.get_singlestore_db_url()
        if db_url.startswith("mysql+pymysql"):
            db_url = "mysql" + db_url[len("mysql+pymysql"):]
        self.clean_url = db_url
    
    def get_latest_trades(self, limit=50):
        query = f"SELECT * FROM live_trades ORDER BY participant_timestamp DESC LIMIT {limit}"
        conn = s2.connect(self.clean_url)
        cur = conn.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            # Extract column names from the cursor description
            col_names = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=col_names)
        finally:
            cur.close()
            conn.close()
        print(df.head())
        return df
