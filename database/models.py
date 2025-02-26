# database/models.py

CREATE_LIVE_TRADES_TABLE = """
CREATE TABLE IF NOT EXISTS live_trades (
    trade_id INT AUTO_INCREMENT PRIMARY KEY,
    localTS VARCHAR(50),
    localDate VARCHAR(50),
    ticker VARCHAR(10),
    conditions VARCHAR(50),
    correction VARCHAR(10),
    exchange VARCHAR(10),
    id VARCHAR(50),
    participant_timestamp BIGINT,
    price FLOAT,
    sequence_number BIGINT,
    sip_timestamp BIGINT,
    size INT,
    tape VARCHAR(10),
    trf_id VARCHAR(50),
    trf_timestamp BIGINT
);
"""
