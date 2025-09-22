FROM python:3.13-alpine

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project configuration files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache --no-dev

# Copy the server code
COPY . .

# Command to run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]