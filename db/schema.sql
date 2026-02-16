-- Main table for valid heartbeats
CREATE TABLE IF NOT EXISTS heartbeats_valid (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    heart_rate INTEGER NOT NULL,
    anomaly BOOLEAN DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_heartbeats_valid_timestamp ON heartbeats_valid (timestamp);

-- Table for invalid or rejected heartbeats
CREATE TABLE IF NOT EXISTS heartbeats_invalid (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    timestamp TIMESTAMPTZ,
    heart_rate INTEGER,
    error_reason TEXT NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_heartbeats_invalid_timestamp ON heartbeats_invalid (timestamp);
