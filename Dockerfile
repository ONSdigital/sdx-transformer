FROM eu.gcr.io/ons-sdx-ci/sdx-gcp:1.3.2
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]