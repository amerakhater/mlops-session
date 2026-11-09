# mlops-session

FastAPI service with a Postgres-backed CRUD API (`/items`) and an OpenAI Q&A endpoint (`/ask`).

## Run

```bash
cp .env.example .env        # then put your real OPENAI_API_KEY in .env
docker compose up -d --build
```

Open http://localhost:8000/docs for the interactive API.

## Endpoints

| Method | Path          | Description                 |
|--------|---------------|-----------------------------|
| GET    | `/health`     | Health check                |
| GET    | `/items`      | List items (`skip`, `limit`)|
| POST   | `/items`      | Create item                 |
| GET    | `/items/{id}` | Get item                    |
| PATCH  | `/items/{id}` | Partially update item       |
| DELETE | `/items/{id}` | Delete item                 |
| POST   | `/ask`        | `{"question": "..."}` → OpenAI answer |

## Layout

```
src/my_project/
  core/config.py         settings from env (pydantic-settings)
  db/session.py          engine, session, Base, table creation
  models/                SQLAlchemy tables
  schemas/               Pydantic request/response validation
  repositories/          database access only
  services/              business logic + OpenAI client
  api/deps.py            dependency wiring
  api/routes/            HTTP endpoints only
  main.py                app setup
```

## CI

[.github/workflows/ci.yml](.github/workflows/ci.yml) runs on pushes to main/development/testing and on every PR:

1. **Lint**: `ruff check` + `ruff format --check`
2. **Tests**: `pytest` against a Postgres service container (OpenAI is faked)
3. **Docker**: `docker compose up --build --wait` + smoke-test the API

Run the same checks locally (Postgres from compose is on host port 55432):

```bash
docker compose up -d db
uv run ruff check . && uv run ruff format --check . && uv run pytest
```

