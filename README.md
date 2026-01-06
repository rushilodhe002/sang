# SentinelStream (Fraud Detection API)

A DEMO-LEVEL Fraud Detection System demonstrating 4 weeks of disciplined backend work.

## Project Overview
**SentinelStream** is a fraud detection API that processes financial transactions, checks for duplicates (idempotency), evaluates risk using a Rule Engine and (simulated) ML model, and persists data to a PostgreSQL database.

## Architecture
- **Framework**: FastAPI (Async)
- **Database**: PostgreSQL (SQLAlchemy Async)
- **Logic**: Rule Engine + Fake ML (Isolation Forest Simulation)
- **Auth**: JWT (Simple implementation)
- **Container**: Dockerized

---

## 📅 4-Week Delivery Components

### Week 1: Planning & Foundation
- Project scaffolding.
- Database Schema (Users, Transactions).
- `GET /health` endpoint.

### Week 2: Core Pipeline
- `POST /transaction` implementation.
- **Idempotency**: Prevents duplicate double-charges via `Idempotency-Key` header.
- Database persistence (AsyncPG).

### Week 3: Intelligence Layer
- **Rule Engine**: Deterministic logic (e.g., Amount > 5000 = Flagged).
- **ML Simulation**: Placeholder for Isolation Forest model.
- Integrated into the transaction flow.

### Week 4: Production Readiness
- **Docker**: `Dockerfile` added.
- **Security**: JWT Authentication for endpoints.
- **Testing**: PyTest cases for health and rules.

---

## 🚀 Setup & Usage

### 1. Prerequisites
- Python 3.9+
- PostgreSQL running locally (DB named `sentinelstream`)

### 2. Installation
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and update your DB credentials (default: `postgres:password@localhost`).

### 4. Running the App
```bash
uvicorn app.main:app --reload
```
Visit Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Authentication
1. Go to `/docs`.
2. Use the **Authorize** button or call `POST /token` with user: `admin`, pass: `admin`.
3. Copy the token and use it for `POST /transaction`.

### 6. Testing
```bash
pytest
```

### 7. Docker Build
```bash
docker build -t sentinel-stream .
docker run -p 8000:8000 sentinel-stream
```
