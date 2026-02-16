

-- Drop old/incorrect tables
DROP TABLE IF EXISTS valid_heartbeat_counts CASCADE;
DROP TABLE IF EXISTS invalid_heartbeat_counts CASCADE;
DROP TABLE IF EXISTS heartbeats_valid CASCADE;
DROP TABLE IF EXISTS heartbeats_invalid CASCADE;

-- Main event table: heartbeats
CREATE TABLE IF NOT EXISTS heartbeats (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    heartbeat_value NUMERIC,
    validation_status VARCHAR NOT NULL CHECK (validation_status IN ('valid', 'invalid_physiological', 'invalid_system', 'corrupted')),
    anomaly_type VARCHAR,
    raw_payload JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT anomaly_type_null_if_valid CHECK (
        (validation_status = 'valid' AND anomaly_type IS NULL)
        OR (validation_status != 'valid')
    )
);
CREATE INDEX IF NOT EXISTS idx_heartbeats_timestamp ON heartbeats (timestamp);
CREATE INDEX IF NOT EXISTS idx_heartbeats_patient_id ON heartbeats (patient_id);

-- Alerts table for derived events
CREATE TABLE IF NOT EXISTS heartbeat_alerts (
    alert_id SERIAL PRIMARY KEY,
    heartbeat_id INTEGER REFERENCES heartbeats(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL,
    patient_id VARCHAR(50),
    heartbeat_value NUMERIC,
    alert_category VARCHAR NOT NULL CHECK (alert_category IN ('physiological_anomaly', 'system_anomaly', 'data_corruption')),
    resolved_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_heartbeat_alerts_timestamp ON heartbeat_alerts (timestamp);
