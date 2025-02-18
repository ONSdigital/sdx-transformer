FROM europe-west2-docker.pkg.dev/ons-sdx-ci/sdx-apps/sdx-gcp:1.4.5

COPY . /app
WORKDIR /app

# Export dependencies to requirements.txt and install them
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "./run.py"]