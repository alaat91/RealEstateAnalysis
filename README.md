# Real Estate Analysis Backend

FastAPI backend starter for a Sweden-focused real estate buy-vs-rent analysis app.

## Stack

- FastAPI
- PostgreSQL + PostGIS
- SQLAlchemy 2.x
- Alembic migrations
- Pydantic v2
- pytest
- Ruff
- GitHub Actions CI

## Local setup

### 1. Clone and enter the repo

```bash
git clone <your-repo-url>
cd realestate-analysis-backend
```

### 2. Create environment file

```bash
cp .env.example .env
```

### 3. Start PostgreSQL/PostGIS and API with Docker

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

### 4. Run migrations

In another terminal:

```bash
docker compose exec api alembic upgrade head
```

### 5. Test health endpoint

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

## Running locally without Docker for the API

Start only the database:

```bash
docker compose up db
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run migrations:

```bash
alembic upgrade head
```

Run the API:

```bash
uvicorn app.main:app --reload
```

## Postman examples

### Health check

```http
GET http://localhost:8000/api/v1/health
```

### Create property

```http
POST http://localhost:8000/api/v1/properties
Content-Type: application/json
```

```json
{
  "title": "3-room apartment in Eriksberg",
  "city": "Göteborg",
  "area": "Eriksberg",
  "address": "Example Street 1",
  "ownership_type": "bostadsratt",
  "property_type": "apartment",
  "asking_price_sek": 3750000,
  "monthly_fee_sek": 5200,
  "living_area_sqm": 72,
  "rooms": 3,
  "latitude": 57.7069,
  "longitude": 11.9389,
  "source_url": "https://example.com/property/1",
  "description": "Example listing for local testing."
}
```

### List properties

```http
GET http://localhost:8000/api/v1/properties?city=Göteborg
```

### Rent-vs-buy analysis

```http
POST http://localhost:8000/api/v1/analyses/rent-vs-buy
Content-Type: application/json
```

```json
{
  "title": "Eriksberg 3-room comparison",
  "purchase_price_sek": 3750000,
  "down_payment_percent": 10,
  "annual_interest_rate_percent": 4.0,
  "monthly_brf_fee_sek": 5200,
  "monthly_rent_sek": 13500,
  "time_horizon_years": 5,
  "expected_annual_price_growth_percent": 2.0,
  "expected_annual_rent_inflation_percent": 2.0,
  "expected_annual_investment_return_percent": 5.0,
  "selling_cost_percent": 2.0,
  "annual_maintenance_percent": 0.3
}
```

## Development commands

```bash
make install
make run
make test
make lint
make format
make migrate
make revision m="add users table"
```

## GitHub setup

1. Create a new repository on GitHub.
2. Push this project.
3. The workflow in `.github/workflows/ci.yml` will run automatically on push and pull requests to `main`.

```bash
git init
git add .
git commit -m "Initial FastAPI backend"
git branch -M main
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

## Next backend features to add

- User authentication
- Saved analyses table and endpoints
- Real Swedish amortization rules
- Swedish interest deduction assumptions
- BRF financial-risk model
- Comparable sold-property matching
- Background jobs with Celery + Redis
- OpenAI/Azure OpenAI report generation
