# Evaluation Mapping

| Evaluation area | Evidence in this project |
|---|---|
| Provision search infrastructure - 25 | OpenSearch service, persistent search volume, index mapping, API indexing/search |
| Environment hardening - 25 | non-root API, read-only root filesystem, no-new-privileges, health checks, resource limits, private network |
| Real-data quality - 20 | PostgreSQL records for companies/jobs/candidates and OpenSearch indexed jobs |
| Live verification - 15 | health endpoint, Docker status, tests and load-test numbers |
| Failure/edge handling - 15 | missing company returns 404, empty search returns 400, health reports degraded state |

## Important limitation

This is a student-scale local/staging demonstration. OpenSearch security is disabled only to keep the local demo simple. A production deployment must enable authentication/TLS and keep OpenSearch private.

The load test is intentionally small. For production capacity planning, use a proper tool such as k6 or Locust against a staging environment.
