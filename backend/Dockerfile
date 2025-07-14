# backend/Dockerfile
# Use a lightweight base Python image
FROM python:3.10-slim

# Set working directory to /app
WORKDIR /app

# Copy the backend requirements file and install dependencies
COPY backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into /app/backend
COPY backend/ /app/backend

# ✅ Add PYTHONPATH so `import backend.xyz` works
ENV PYTHONPATH=/app

# Run FastAPI app using uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
