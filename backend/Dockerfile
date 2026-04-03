FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /build

COPY backend/pyproject.toml .
COPY backend/main.py ./backend/

RUN uv build --wheel --out-dir /dist


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /dist/*.whl .

RUN pip install --no-cache-dir *.whl && rm *.whl

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]