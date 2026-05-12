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

EXPOSE 8080

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
