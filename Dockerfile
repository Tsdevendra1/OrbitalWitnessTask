FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

# Using "dev" instead of "run" to run in local mode, can be changed to "run" for production
CMD ["/app/.venv/bin/fastapi", "dev", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]