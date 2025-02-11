FROM europe-west2-docker.pkg.dev/ons-sdx-ci/sdx-apps/sdx-gcp:1.4.4

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