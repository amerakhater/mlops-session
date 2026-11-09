from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from my_project.db.session import engine
from my_project.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    # Entering the client runs the app lifespan, which creates the tables.
    with TestClient(app) as c:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE items RESTART IDENTITY"))
        yield c
    app.dependency_overrides.clear()
