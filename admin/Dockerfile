FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m pip install --no-cache-dir poetry

ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-interaction --no-ansi

COPY . /app

FROM python:3.11-slim

WORKDIR /app/admin

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
