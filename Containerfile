FROM docker.io/library/python:3.12.2-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir --disable-pip-version-check -r /app/requirements.txt

COPY entrypoint.sh metrx.py /app
COPY utils /app/utils
COPY modules /app/modules

VOLUME /config
VOLUME /app/modules/custom

ENTRYPOINT ["/app/entrypoint.sh"]