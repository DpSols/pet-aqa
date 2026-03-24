# Pet Automation — Multi-Platform Testing Framework

A demonstration of architectural best practices in test automation using Python, testing **APIs**, **web applications**, and **mobile apps**.

## Platforms & Stack

| Layer | Technology |
|---|---|
| Test Runner | Pytest 8.3 |
| API Testing | Requests + Pydantic models |
| Web Testing | Playwright 1.50 (Chromium) |
| Mobile Testing | Appium 4.3 |
| Infrastructure | PostgreSQL 16, Kafka 7.6 (KRaft) |
| Database ORM | SQLAlchemy 2.0.48 |
| Reporting | Allure 2.13 |
| Logging | Loguru 0.7 |

## What It Demonstrates

- **Protocol-Based Architecture**: Structural typing via `typing.Protocol` — zero inheritance coupling
- **Layered Separation**: Tests → Steps → Clients/Page Objects → Infrastructure → Protocols
- **Generic Repository Pattern**: Type-safe `PostgresRepository[T]` for any Pydantic model
- **BDD-Style Steps**: Reusable `@allure.step` decorated test steps with narrative flow
- **Infrastructure Integration**: Real Kafka producer/consumer and PostgreSQL persistence
- **Custom Pytest Plugins**: Automatic logging and Allure metadata writers
- **Configuration Management**: Hierarchical settings (defaults → `.env` → env vars)
- **Docker Support**: Containerized runner + Docker Compose for local services

## Quick Start

```bash
# Install dependencies
pip install -r requirements-dev.txt
playwright install --with-deps chromium

# Start local services (Kafka + PostgreSQL)
docker compose -f docker/docker-compose.yml up -d

# Run tests
pytest tests/api/ -v --alluredir=allure-results
pytest tests/web/ -v
pytest tests/mobile/ -v

# View report
allure serve allure-results
```

## Key Files

| File | Purpose |
|---|---|
| `core/protocols.py` | Contracts (StorageRepository, MessageProducer, MessageConsumer) |
| `infrastructure/` | Concrete implementations (PostgreSQL, Kafka) |
| `src/api/`, `src/web/`, `src/mobile/` | Clients, page objects, screen objects |
| `src/steps/` | BDD test steps (orchestration) |
| `tests/` | Test suites organized by platform |

## Design Highlights

✅ **Protocol-first** — All major dependencies defined as structural contracts
✅ **Type-safe** — Full mypy strict mode compliance
✅ **Parallel execution** — pytest-xdist for fast test runs
✅ **Rich reporting** — Allure + custom environment + failure categories
✅ **Testable steps** — Plain classes, independently testable
✅ **CI/CD ready** — 3-stage GitLab pipeline (lint → api → web)