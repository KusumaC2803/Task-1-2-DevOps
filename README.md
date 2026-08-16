# Task 1 - Company Onboarding & Marketplace Data Model

DevOps Engineer | PlaceMux | Phase 2

This project is a small, runnable demo of the infrastructure needed for a marketplace:
- PostgreSQL for marketplace data
- OpenSearch for job search
- FastAPI service for company/job/candidate operations
- Docker Compose for repeatable local/staging setup
- health checks and resource limits
- environment-based configuration (no secrets in source code)
- GitHub Actions CI for tests
- a small Python load test
- a simple rollback/runbook

## 1. Project structure

```text
app/                 API and database/search code
tests/               basic API tests
scripts/             seed and load-test scripts
infra/               environment configuration
.github/workflows/   CI pipeline
docker-compose.yml   local/staging stack
.env.example         safe configuration template
```

## 2. Run it

Prerequisite: Docker Desktop.

```bash
copy .env.example .env
docker compose up --build -d
docker compose ps
```

The API is available at:

```text
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health
```

OpenSearch is intentionally not exposed outside the local machine through the application. It is reachable by the API at `http://opensearch:9200`.

## 3. Seed demo data

```bash
docker compose exec api python scripts/seed_data.py
```

Then try:

```text
GET /companies
GET /jobs
GET /jobs/search?q=python
GET /candidates
```

A company can be created with:

```text
POST /companies
{
  "name": "Demo Technologies",
  "email": "hr@demo-tech.example"
}
```

A job can be created with:

```text
POST /jobs
{
  "company_id": 1,
  "title": "Python Backend Developer",
  "description": "Python, FastAPI and PostgreSQL",
  "skills": ["python", "fastapi", "postgresql"]
}
```

## 4. Test

```bash
docker compose exec api pytest -q
```

Expected result: all tests pass.

## 5. Search check

```bash
curl "http://localhost:8000/jobs/search?q=python"
```

The API writes jobs to PostgreSQL and indexes them into OpenSearch. Search results therefore come from the search service rather than filtering a hard-coded list.

## 6. Capacity check

Run:

```bash
python scripts/load_test.py
```

The script sends repeated search requests and prints request count, failures and average latency. This is a small local capacity check, not a production benchmark.

## 7. Environment hardening included

- secrets/configuration are read from environment variables
- `.env` is ignored by Git
- containers use health checks
- API runs as a non-root user
- API container has a read-only root filesystem with a temporary writable directory
- service dependencies wait for healthy database/search services
- PostgreSQL and OpenSearch are on a private Docker network
- basic resource limits are set
- CI runs tests before a deployment step would be added

## 8. Rollback

For this local demo, the simplest rollback is to return to the previous image/tag and restart the stack:

```bash
docker compose down
docker compose up -d
```

For a real cloud deployment, images should be tagged with a commit SHA and the previous known-good image should be redeployed.

## 9. Evidence for evaluation

During the demo, show:

1. `docker compose ps` with healthy services.
2. `/health` response.
3. A company being created.
4. A job being created.
5. `/jobs/search?q=python` returning the created job.
6. `pytest -q` passing.
7. `python scripts/load_test.py` showing request/latency numbers.
8. `.env.example` and `.gitignore` to show secrets are not committed.
9. GitHub Actions run passing.

This keeps the demonstration based on actual running services and numbers rather than claims.
