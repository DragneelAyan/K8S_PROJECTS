# ============================
#       BUILDER STAGE
# ============================
FROM python:3.10-slim AS builder
# "builder" is our construction zone.
# This image contains compilers and tools only needed to *build* dependencies,
# not to actually run the app. Keeps final image much smaller.


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# - PYTHONDONTWRITEBYTECODE=1  → prevents Python from generating .pyc files. Saves space.
# - PYTHONUNBUFFERED=1         → ensures real-time logging inside containers.


WORKDIR /app
# Set working directory where all build operations happen.

# Install OS-level packages needed only for building Python wheels.
# build-essential + gcc let pip compile packages that contain native extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*
# Clean-up after apt so the layer remains small.


COPY requirements.txt .
# Copy *just* dependency file. This is critical for Docker caching.
# Docker will install dependencies once, and reuse that layer until requirements.txt changes.


RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
# Pre-build wheels for all dependencies.
# Wheels are precompiled binary packages → faster installation in runtime stage.
# Output is stored in /wheels so we can reuse it later.


COPY . .
# Copy the rest of your application code into the builder stage.




# ============================
#       RUNTIME STAGE
# ============================
FROM python:3.10-slim AS runtime
# Fresh image without compilers, making your final container lighter and safer.


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_MESSAGE="Hello from GitOps!"
# Carry over Python runtime settings.
# Add your custom environment variable used by the app.


WORKDIR /app
# Application root directory during runtime.


# Install lightweight utilities only (curl is optional).
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
# No compilers or build tools here — runtime stays clean.


COPY --from=builder /wheels /wheels
# Pull prebuilt wheels from builder → no need for gcc in this stage.


RUN pip install --no-cache /wheels/*
# Install dependencies directly from wheels → super fast, no compilation, no cache bloat.


COPY . .
# Copy only your application files.
# This ensures the runtime image does NOT include build artifacts from builder.


EXPOSE 8080
# Container exposes port 8080 (informational for orchestration systems like Kubernetes).


# Best practice: never run Python apps as root inside containers.
RUN useradd -m appuser
USER appuser
# Creates a dedicated non-root user and switches to it.
# Prevents privilege escalation attacks and satisfies DevSecOps checks.


CMD ["python", "app.py"]
# Container startup command.
# Using exec form ensures proper signal handling (important for graceful shutdown in Kubernetes).
