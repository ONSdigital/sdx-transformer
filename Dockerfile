FROM python:3.13-slim

RUN python -m pip install --upgrade pip

# Install Poetry using pip
RUN pip install poetry

# Set PATH to include Poetry
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY . /app
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root

EXPOSE 5000
CMD ["python", "./run.py"]