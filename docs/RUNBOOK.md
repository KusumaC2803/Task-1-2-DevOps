# Task 1 Runbook

## Start

1. Copy `.env.example` to `.env`.
2. Change the local database password.
3. Run `docker compose up --build -d`.
4. Check `docker compose ps`.
5. Check `http://localhost:8000/health`.

## Search provisioning

OpenSearch is provisioned by `docker-compose.yml`. Its data is stored in the `search_data` named volume, so restarting the container does not remove the index.

The API creates the `jobs` index when the first job is indexed.

## Company onboarding test

1. Create a company.
2. Create a job for that company.
3. Search for a skill such as `python`.
4. Confirm the job is returned.

## Failure check

Stop OpenSearch:

```bash
docker compose stop opensearch
```

The API health endpoint should report degraded search status.

Start it again:

```bash
docker compose start opensearch
```

Then verify:

```text
GET /health
```

## Rollback

Keep the last known-good image tag in a deployment registry. To roll back, deploy that image and restart the service. For this local task, rebuilding from the previous Git commit is enough:

```bash
git checkout <known-good-commit>
docker compose up --build -d
```

## What to show the evaluator

- healthy containers
- health endpoint
- real company record
- real job record
- search result
- passing tests
- load-test output
- CI result
- no real secrets in the repository
