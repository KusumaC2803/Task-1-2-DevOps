# 2-minute demo flow

1. `docker compose ps`
2. Open `/health` and show database/search are healthy.
3. Create a company in `/docs`.
4. Create a job for that company.
5. Search `/jobs/search?q=python`.
6. Run `docker compose exec api pytest -q`.
7. Run `python scripts/load_test.py`.
8. Show the GitHub Actions CI run.

Keep the explanation simple: "PostgreSQL stores marketplace records. OpenSearch handles job discovery. Docker Compose makes the environment repeatable. Health checks and hardening reduce deployment and recovery problems."
