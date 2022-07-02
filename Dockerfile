### Build and install packages
FROM python:3.8 as build-python

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

### Final image
FROM python:3.8-slim

RUN groupadd -r crm && useradd -r -g crm crm

COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app

EXPOSE 8000
ENV PYTHONUNBUFFERED 1

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PYTHONPATH=.

LABEL org.opencontainers.image.title="srubtsov/crm"                                     \
      org.opencontainers.image.description="A Personal CRM system for your IT business" \
      org.opencontainers.image.source="https://github.com/srubtsov/crm"                  \
      org.opencontainers.image.revision="$COMMIT_ID"                                     \
      org.opencontainers.image.version="$PROJECT_VERSION"

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./config/gunicorn_config.py",  "crm.services.main:app"]
