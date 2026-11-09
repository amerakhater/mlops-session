FROM python:3.12-slim

# Install uv (pinned to match the local toolchain)
COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Install dependencies first (cached layer while only code changes)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the source and install the project itself
COPY src ./src
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "my_project.main:app", "--host", "0.0.0.0", "--port", "8000"]
