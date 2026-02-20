# Stage 1: Builder - install Python dependencies
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Install system dependencies (Node.js for opencode, git for repos)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl git ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g opencode 2>/dev/null || echo "opencode install skipped" && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# Copy application
WORKDIR /app
COPY . .

# Create output directories
RUN mkdir -p /docs/docs/generated /docs/docs/manual

# Make scripts executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["generate"]
