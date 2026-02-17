-- ============================================================================
-- GRAFANA DASHBOARD SQL QUERIES
-- Heartbeat Monitoring System
-- ============================================================================

-- Panel 1: Total Heartbeats (Stat)
SELECT COUNT(*) AS total_heartbeats FROM heartbeats;

-- Panel 2: Valid vs Invalid (Pie Chart)
SELECT validation_status AS status, COUNT(*) AS count 
FROM heartbeats 
GROUP BY validation_status;

-- Panel 3: Anomalies Breakdown (Pie/Bar)
SELECT anomaly_type AS type, COUNT(*) AS count 
FROM heartbeats 
WHERE validation_status != 'valid' 
GROUP BY anomaly_type;

-- Panel 4: Active Alerts (Stat)
SELECT COUNT(*) AS active_count 
FROM heartbeat_alerts 
WHERE resolved_flag = false;

-- Panel 5: Alerts Over Time (Time Series)
SELECT DATE_TRUNC('minute', timestamp) AS time, COUNT(*) AS alert_count 
FROM heartbeat_alerts 
WHERE resolved_flag = false 
GROUP BY time 
ORDER BY time;

-- Panel 5B: Alerts Over Time by Category (Multi-Line)
SELECT DATE_TRUNC('minute', timestamp) AS time, alert_category, COUNT(*) AS alert_count 
FROM heartbeat_alerts 
WHERE resolved_flag = false 
GROUP BY time, alert_category 
ORDER BY time;

-- Panel 6: Heartbeat Trends (Time Series)
SELECT DATE_TRUNC('minute', timestamp) AS time, 
    AVG(heartbeat_value) AS avg_heartbeat, 
    MIN(heartbeat_value) AS min_heartbeat, 
    MAX(heartbeat_value) AS max_heartbeat 
FROM heartbeats 
GROUP BY time 
ORDER BY time;

-- Panel 7: Recent Alerts (Table)
SELECT timestamp, patient_id, heartbeat_value, alert_category, resolved_flag 
FROM heartbeat_alerts 
ORDER BY timestamp DESC 
LIMIT 50;

-- Panel 8: Top Patients with Anomalies (Bar Chart)
SELECT patient_id, COUNT(*) AS anomaly_count 
FROM heartbeats 
WHERE validation_status != 'valid' 
GROUP BY patient_id 
ORDER BY anomaly_count DESC 
LIMIT 10;

-- ============================================================================
-- ALERT RULES
-- ============================================================================

-- Alert: Critical Physiological Anomaly
SELECT COUNT(*) FROM heartbeat_alerts 
WHERE alert_category = 'physiological_anomaly' AND resolved_flag = false;

-- Alert: System Anomaly
SELECT COUNT(*) FROM heartbeat_alerts 
WHERE alert_category = 'system_anomaly' AND resolved_flag = false;

-- Alert: Corrupted Data
SELECT COUNT(*) FROM heartbeats WHERE validation_status = 'corrupted';

-- ============================================================================
-- OPTIONAL QUERIES
-- ============================================================================

-- Active Alerts by Category
SELECT alert_category AS category, COUNT(*) AS active_count 
FROM heartbeat_alerts 
WHERE resolved_flag = false 
GROUP BY alert_category;

-- Average Heartbeat per Patient
SELECT patient_id, AVG(heartbeat_value) AS avg_heartbeat 
FROM heartbeats 
WHERE validation_status = 'valid' 
GROUP BY patient_id 
ORDER BY avg_heartbeat DESC;

-- Alert Resolution Statistics
SELECT alert_category, 
    COUNT(*) AS total_alerts,
    COUNT(*) FILTER (WHERE resolved_flag = true) AS resolved_count,
    COUNT(*) FILTER (WHERE resolved_flag = false) AS unresolved_count
FROM heartbeat_alerts 
GROUP BY alert_category;

-- Activity by Hour
SELECT EXTRACT(HOUR FROM timestamp) AS hour_of_day, COUNT(*) AS event_count 
FROM heartbeats 
GROUP BY hour_of_day 
ORDER BY hour_of_day;

-- Patients with Mixed Status
SELECT patient_id,
    COUNT(*) FILTER (WHERE validation_status = 'valid') AS valid_count,
    COUNT(*) FILTER (WHERE validation_status != 'valid') AS invalid_count
FROM heartbeats
GROUP BY patient_id
HAVING COUNT(*) FILTER (WHERE validation_status = 'valid') > 0
   AND COUNT(*) FILTER (WHERE validation_status != 'valid') > 0
ORDER BY invalid_count DESC;
