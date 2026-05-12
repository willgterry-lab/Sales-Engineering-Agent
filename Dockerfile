FROM python:3.11-slim

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first so Docker can cache the install layer
COPY pyproject.toml uv.lock README.md ./

# Install production dependencies only
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ ./src/
COPY fixtures/ ./fixtures/
COPY app.py ./

EXPOSE 8501

# Railway injects $PORT at runtime; fall back to 8501 locally
CMD ["sh", "-c", "uv run streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]
