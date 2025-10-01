FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache git

# Install uv
RUN pip install uv

# Copy project configuration files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --no-cache --no-dev

# Copy the server code
COPY . .

# Command to run the application using uv run
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]