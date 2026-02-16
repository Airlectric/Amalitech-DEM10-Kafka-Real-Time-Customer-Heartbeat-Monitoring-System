# Real-Time Customer Heartbeat Monitoring System: Complete Setup Guide

## Prerequisites
- Docker & Docker Compose installed
- Python 3.10+ installed
- (Optional) Git for version control

---

## 1. Clone the Project
```sh
git clone <your-repo-url>
cd Amalitech-DEM10-Kafka-Real-Time-Customer-Heartbeat-Monitoring-System
```

---

## 2. Environment Variables
- Copy `.env.example` to `.env` and adjust values as needed:
```sh
cp .env.example .env
```
- Edit `.env` to set your PostgreSQL and Grafana credentials if desired.

---

## 3. Start the Infrastructure
- Start all services (Kafka, Zookeeper, PostgreSQL, Grafana):
```sh
docker compose up -d
```
- Wait for all containers to be healthy.

---

## 4. Initialize the Database Schema
- Run the following to create all tables and indexes:
```sh
python src/main.py --init-db
```

---

## 5. Run the Data Pipeline
- To run the producer (sends data to Kafka):
```sh
python src/main.py --producer
```
- To run the consumer (reads from Kafka, writes to DB):
```sh
python src/main.py --consumer
```
- To run both at once (in the same terminal):
```sh
python src/main.py --both
```

---

## 6. Access Grafana Dashboard
- Open [http://localhost:3000](http://localhost:3000)
- Login with user `admin` and the password from your `.env` file (default: `admin`)
- Add PostgreSQL as a data source:
  - Host: `postgres:5432`
  - Database, user, password: from your `.env`
- Create dashboards to visualize heartbeats from the `heartbeats_valid` and `heartbeats_invalid` tables.

---

## 7. Run Automated Tests
- To check the data generator:
```sh
python -m unittest tests/test_data_generator.py
```
- To check the producer logic:
```sh
python -m unittest tests/test_producer.py
```
- To check the consumer logic:
```sh
python -m unittest tests/test_consumer.py
```

---

## 8. Logs
- All logs are stored in the `logs/` directory:
  - `general.log`: All logs
  - `error.log`: Errors only
  - `info.log`: Info messages
  - `warning.log`: Warnings

---

## 9. Stopping the System
- To stop all services:
```sh
docker compose down
```

---

## 10. Troubleshooting
- If containers fail to start, check logs with:
```sh
docker compose logs <service>
```
- If you change `.env`, restart services:
```sh
docker compose down && docker compose up -d
```
- For database or Kafka issues, check the respective logs in Docker or the `logs/` folder.

---

## 11. Project Structure Overview
```
project-root/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env / .env.example
├── db/
│   └── schema.sql
├── src/
│   ├── config/
│   ├── data/
│   ├── kafka/
│   ├── db/
│   └── main.py
├── logs/
├── tests/
├── docs/
└── notes/
```

---

## 12. Additional Notes
- You can extend the system with dashboards (Grafana), alerting, or more advanced analytics.
- All code is modular and beginner-friendly, with explanations in the `notes/` folder.
- For any issues, check the logs and documentation first.

---

## 13. Support
- For help, review the markdown files in `notes/` for beginner-friendly explanations of each module and feature.
- If you need more help, ask your instructor or team lead.
