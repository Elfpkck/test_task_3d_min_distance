FROM python:3.14-slim

# Install uv package manager
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Set the default command
CMD ["uv", "run", "python", "distance_calculator.py"]
