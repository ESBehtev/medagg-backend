#############################
# Stage 1: Base build stage #
#############################
FROM python:3.13-slim AS builder

RUN mkdir /app
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install requirements
RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

#############################
# Stage 2: Production stage #
#############################
FROM python:3.13-slim AS prod

RUN useradd -m -r djangouser && \
    mkdir /app && \
    chown -R djangouser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

# Copy source code
COPY --chown=djangouser:djangouser src/ .

# Same Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER djangouser
